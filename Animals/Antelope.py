from Animal import Animal


class Antelope(Animal):
    def __init__(self, strength, initiative, x, y, gameWorld):
        super().__init__(strength, initiative, x, y, gameWorld)

    def __str__(self):
        return "Antelope"

    def getName(self):
        return "Antelope"

    def getSteps(self):
        return 2

    def getID(self):
        return 2