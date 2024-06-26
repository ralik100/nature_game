from World import World # type: ignore
from Position import Position # type: ignore
from Organisms.Grass import Grass # type: ignore
from Organisms.Sheep import Sheep # type: ignore
from Organisms.Rys import Rys # type: ignore
from Organisms.Antylopa import Antylopa # type: ignore
import os


if __name__ == '__main__':
	pyWorld = World(10, 10)

	newOrg = Grass(position=Position(xPosition=9, yPosition=9), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Grass(position=Position(xPosition=1, yPosition=1), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Sheep(position=Position(xPosition=2, yPosition=2), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Rys(position=Position(xPosition=5, yPosition=2), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Antylopa(position=Position(xPosition=9, yPosition=3), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	print(pyWorld)

	for _ in range(0, 50):
		input('')
		os.system('cls')
		pyWorld.makeTurn()		
		print(pyWorld)
		
		