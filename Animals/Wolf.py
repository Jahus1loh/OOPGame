from Animal import Animal


class Wolf(Animal):
    def __init__(self, strength, initiative, x, y, gameWorld):
        super().__init__(strength, initiative, x, y, gameWorld)

    def getName(self):
        return "Wolf"

    def getID(self):
        return 11