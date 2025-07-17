import random

from Plant import Plant


class Sosnowsky(Plant):
    def __init__(self, strength, initiative, x, y, gameWorld):
        super().__init__(strength, initiative, x, y, gameWorld)
        self.rand = random.Random()
        self.gameWorld = gameWorld

    def getName(self):
        return "Sosnowsky"

    def getID(self):
        return 8

    def isPlant(self):
        return True
