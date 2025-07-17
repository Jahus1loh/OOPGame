import random

from Commentator import Commentator
import GameConstants
from Organism import Organism


class Animal(Organism):
    def __init__(self, strength, initiative, x, y, gameWorld):
        super().__init__(strength, initiative, x, y, gameWorld)
        self.gameWorld = gameWorld

    def action(self):
        randomNumber = random.randint(1, 4)
        newX = 0
        newY = 0
        if randomNumber == 1:
            if self.x > self.getSteps() - 1:
                newX = self.x - self.getSteps()
            else:
                newX = self.x
            newY = self.y
        elif randomNumber == 2:
            if self.y > self.getSteps() - 1:
                newY = self.y - self.getSteps()
            else:
                newY = self.y
            newX = self.x
        elif randomNumber == 3:
            if self.x < GameConstants.SQUARE_NUMBERS - self.getSteps():
                newX = self.x + self.getSteps()
            else:
                newX = self.x
            newY = self.y
        elif randomNumber == 4:
            if self.y < GameConstants.SQUARE_NUMBERS - self.getSteps():
                newY = self.y + self.getSteps()
            else:
                newY = self.y
            newX = self.x
        else:
            newX = self.x
            newY = self.y

        if (self.x != newX or self.y != newY) and self.gameWorld.isOccupied(newX, newY):
            defender = self.gameWorld.getOrganism(newX, newY)
            if defender is not None:
                self.collision(self, defender)

        self.gameWorld.moveOrganism(self.x, self.y, newX, newY)
        self.x = newX
        self.y = newY

    def getSteps(self):
        return 1

    def getName(self):
        return None

    def escape(self):
        return False

    def isPlant(self):
        return False

    def getID(self):
        return 0

    @staticmethod
    def inBounds(x, y):
        return 0 <= x < GameConstants.SQUARE_NUMBERS and 0 <= y < GameConstants.SQUARE_NUMBERS

