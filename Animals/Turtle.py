import random
import GameConstants
from Animal import Animal


class Turtle(Animal):
    def __init__(self, strength, initiative, x, y, gameWorld):
        super().__init__(strength, initiative, x, y, gameWorld)
        self.gameWorld = gameWorld

    def getName(self):
        return "Turtle"

    def getId(self):
        return 10

    def action(self):
        randomNum = random.randint(1, 16)
        newX, newY = self.x, self.y

        if randomNum == 1:
            if self.x > self.getSteps() - 1:
                newX = self.x - self.getSteps()
        elif randomNum == 2:
            if self.y > self.getSteps() - 1:
                newY = self.y - self.getSteps()
        elif randomNum == 3:
            if self.x < GameConstants.SQUARE_NUMBERS - self.getSteps():
                newX = self.x + self.getSteps()
        elif randomNum == 4:
            if self.y < GameConstants.SQUARE_NUMBERS - self.getSteps():
                newY = self.y + self.getSteps()

        if (self.x != newX or self.y != newY) and self.gameWorld.isOccupied(newX, newY):
            defender = self.gameWorld.getOrganism(newX, newY)
            if defender is not None:
                self.collision(self, defender)

        print(f"Organism moved from {self.x} {self.y} to position {newX} {newY}")
        self.gameWorld.moveOrganism(self.x, self.y, newX, newY)
        self.setX(newX)
        self.setY(newY)
