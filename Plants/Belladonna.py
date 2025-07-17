import random
from Plant import Plant


class Belladonna(Plant):
    def __init__(self, strength, inititative, x, y, gameWorld):
        super().__init__(strength, inititative, x, y, gameWorld)
        self.rand = random.Random()
        self.gameWorld = gameWorld

    def getName(self):
        return "Belladonna"

    def getID(self):
        return 3

    def isPlant(self):
        return True
