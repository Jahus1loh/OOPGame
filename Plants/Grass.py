import random

from Plant import Plant


class Grass(Plant):
    def __init__(self, strength, initiative, x, y, gameWorld):
        super().__init__(strength, initiative, x, y, gameWorld)
        self.rand = random.Random()
        self.gameWorld = gameWorld

    def getName(self):
        return "Grass"

    def getID(self):
        return 5

    def isPlant(self):
        return True
