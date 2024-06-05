from Position import Position
from Organisms.Plant import Plant
from Action import Action
from ActionEnum import ActionEnum
from Organisms.Grass import Grass 
from Organisms.Sheep import Sheep 
from Organisms.Rys import Rys 
from Organisms.Antylopa import Antylopa 
import random

class World(object):

	def __init__(self, worldX, worldY):
		self.__worldX = worldX
		self.__worldY = worldY
		self.__turn = 0
		self.__organisms = []
		self.__newOrganisms = []
		self.__separator = '.'
		self.__plague = False
		self.__countdown = 2

	@property
	def worldX(self):
		return self.__worldX

	@property
	def worldY(self):
		return self.__worldY

	@property
	def turn(self):
		return self.__turn

	@turn.setter
	def turn(self, value):
		self.__turn = value

	@property
	def organisms(self):
		return self.__organisms

	@organisms.setter
	def organisms(self, value):
		self.__organisms = value

	@property
	def newOrganisms(self):
		return self.__newOrganisms

	@newOrganisms.setter
	def newOrganisms(self, value):
		self.__newOrganisms = value

	@property
	def separator(self):
		return self.__separator

	def makeTurn(self):
		
		actions = []
		print("jesli chcesz wlaczyc tryb plagii, to wybierz 1")
		print("jesli chcesz dodac nowy organizm, to wybierz 2")
		try:
			pick=int(input("wpisz:"))
		except ValueError:
			pass
		try:
			match pick:
				case 1:
					if not self.__plague:
						for org in self.organisms:
							if self.positionOnBoard(org.position):
								actions = org.decreasehealth()
				
								for a in actions:
									self.makeMove(a)
								actions=[]
						self.__plague = True
					else:
						print("")
						print("plaga pustoszy juz swiat")
						print("")
				case 2:
					result=[]
					#fields=ob
					print("1 - Grass")
					print("2 - Rys")
					print("3 - Sheep")
					print("4 - Antylopa")
					
					name=int(input("jaki organizm chcialbys dodac?: "))

					pos_x=int(input("podaj x: "))
					pos_y=int(input("podaj y: "))
					
					match name:
						case 1:
							newOrg = Grass(position=Position(xPosition=pos_x, yPosition=pos_y), world=self)
							self.addOrganism(newOrg)
						case 2:
							newOrg = Rys(position=Position(xPosition=pos_x, yPosition=pos_y), world=self)
							self.addOrganism(newOrg)
						case 3:
							newOrg = Sheep(position=Position(xPosition=pos_x, yPosition=pos_y), world=self)
							self.addOrganism(newOrg)
						case 4:
							newOrg = Antylopa(position=Position(xPosition=pos_x, yPosition=pos_y), world=self)
							self.addOrganism(newOrg)
						case _:
							print("niepoprawne dane wejsciowe")
					
				case _:
					print("niepoprawne dane wejsciowe")		
		except UnboundLocalError:
			pass
		for org in self.organisms:
			if self.positionOnBoard(org.position):
				actions = org.move()
				for a in actions:
					self.makeMove(a)
				actions = []
				if self.positionOnBoard(org.position):
					actions = org.action()
					for a in actions:
						self.makeMove(a)
					actions = []


		
		self.organisms = [o for o in self.organisms if self.positionOnBoard(o.position)]
		for o in self.organisms:
			o.liveLength -= 1
			o.power += 1
			if o.liveLength < 1:
				print(str(o.__class__.__name__) + ': died of old age at: ' + str(o.position))
		self.organisms = [o for o in self.organisms if o.liveLength > 0]

		self.newOrganisms = [o for o in self.newOrganisms if self.positionOnBoard(o.position)]
		self.organisms.extend(self.newOrganisms)
		self.organisms.sort(key=lambda o: o.initiative, reverse=True)
		self.newOrganisms = []

		if self.__plague and self.__countdown>0:
			self.__countdown-=1
		elif self.__plague and self.__countdown==0:
			for org in self.organisms:
				if self.positionOnBoard(org.position):
					actions = org.increasehealth()
				
					for a in actions:
						self.makeMove(a)
			print("")
			print("plaga konczy sie")
			print("")
			self.__plague=False
			self.__countdown=2
		


		self.turn += 1

	def makeMove(self, action):
		print(action)
		if action.action == ActionEnum.A_ADD:
			self.newOrganisms.append(action.organism)
		elif action.action == ActionEnum.A_INCREASEPOWER:
			action.organism.power += action.value
		elif action.action == ActionEnum.A_MOVE:
			action.organism.position = action.position
		elif action.action == ActionEnum.A_REMOVE:
			action.organism.position = Position(xPosition=-1, yPosition=-1)
		elif action.action == ActionEnum.A_DECREASELIVELENGTH:
			action.organism.liveLength -= action.value
		elif action.action == ActionEnum.A_INCREASELIVELENGTH:
			action.organism.liveLength += action.value

	def addOrganism(self, newOrganism):
		newOrgPosition = Position(xPosition=newOrganism.position.x, yPosition=newOrganism.position.y)

		if self.positionOnBoard(newOrgPosition):
			self.organisms.append(newOrganism)
			self.organisms.sort(key=lambda org: org.initiative, reverse=True)
			return True
		return False

	def positionOnBoard(self, position):
		return position.x >= 0 and position.y >= 0 and position.x < self.worldX and position.y < self.worldY

	def getOrganismFromPosition(self, position):
		pomOrganism = None

		for org in self.organisms:
			if org.position == position:
				pomOrganism = org
				break
		if pomOrganism is None:
			for org in self.newOrganisms:
				if org.position == position:
					pomOrganism = org
					break
		return pomOrganism

	def getNeighboringPositions(self, position):
		result = []
		pomPosition = None

		for y in range(-1, 2):
			for x in range(-1, 2):
				pomPosition = Position(xPosition=position.x + x, yPosition=position.y + y)
				if self.positionOnBoard(pomPosition) and not (y == 0 and x == 0):
					result.append(pomPosition)
		return result

	def filterFreePositions(self, fields):
		result = []

		for field in fields:
			if self.getOrganismFromPosition(field) is None:
				result.append(field)
		return result

	def filterPositionsWithoutAnimals(self, fields):
		result = []
		pomOrg = None

		for filed in fields:
			pomOrg = self.getOrganismFromPosition(filed)
			if pomOrg is None or isinstance(pomOrg, Plant):
				result.append(filed)
		return result

	def __str__(self):
		result = '\nturn: ' + str(self.__turn) + '\n'
		for wY in range(0, self.worldY):
			for wX in range(0, self.worldX):
				org = self.getOrganismFromPosition(Position(xPosition=wX, yPosition=wY))
				if org:
					result += str(org.sign)
				else:
					result += self.separator
			result += '\n'
		return result

	#def near_rys(self, org):
		pomPos = org.getNeighboringPosition()
		result=[]
		no_rys_pomPos = pomPos
		try:
			pos=no_rys_pomPos.index(Rys)
			no_rys_pomPos.pop(pos)
		except IndexError:
			pass
		if	pomPos.getOrganismFromPosition()==Rys and len(no_rys_pomPos)>0 and org.position.getOrganismFromPosition()==Antylopa:
				newPosition = random.choice(no_rys_pomPos+1)
				result.append(Action(ActionEnum.A_MOVE, newPosition, 0, org))
				org.lastPosition = org.position
				metOrganism = org.world.getOrganismFromPosition(newPosition)
				if metOrganism is not None : 
					result.extend(metOrganism.consequences(org))
		return result