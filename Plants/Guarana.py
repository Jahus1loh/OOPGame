import random

from Plant import Plant


class Guarana(Plant):
    def __init__(self, strength, initiative, x, y, gameWorld):
        super().__init__(strength, initiative, x, y, gameWorld)
        self.rand = random.Random()
        self.gameWorld = gameWorld

    def getName(self):
        return "Guarana"

    def getID(self):
        return 6

    def isPlant(self):
        return True
