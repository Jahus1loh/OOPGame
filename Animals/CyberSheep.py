from Animal import Animal
from math import sqrt
import random
from GameConstants import SQUARE_NUMBERS


class CyberSheep(Animal):
    def __init__(self, strength, initiative, x, y, gameWorld):
        super().__init__(strength, initiative, x, y, gameWorld)
        self.gameWorld = gameWorld
        self.allSosnowsky = []

    def getName(self):
        return "CyberSheep"

    def getID(self):
        return 12

    def action(self):
        self.find_closest_sosnowsky()

    def findAllSosnowsky(self):
        organisms = self.gameWorld.getOrganismsOnBoard()
        for organism in organisms:
            if organism.getName() == "Sosnowsky":
                self.allSosnowsky.append(organism)

    def find_closest_sosnowsky(self):
        self.findAllSosnowsky()
        minDist = 100
        towardsX = -1
        towardsY = -1
        newX = -1
        newY = -1
        for organism in self.allSosnowsky:
            dist = sqrt(pow(self.x + organism.getX(), 2) + pow(self.y + organism.getY(), 2))
            if dist < minDist:
                towardsX = organism.getX()
                towardsY = organism.getY()
                minDist = dist

        if towardsX != -1 and towardsY != -1:
            if towardsX > self.x:
                newX = self.x + 1
            elif towardsX < self.x:
                newX = self.x - 1
            elif towardsX == self.x:
                newX = self.x

            if towardsY > self.y:
                newY = self.y + 1
            elif towardsY < self.y:
                newY = self.y - 1
            elif towardsY == self.y:
                newY = self.y
        else:
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
                if self.x < SQUARE_NUMBERS - self.getSteps():
                    newX = self.x + self.getSteps()
                else:
                    newX = self.x
                newY = self.y
            elif randomNumber == 4:
                if self.y < SQUARE_NUMBERS - self.getSteps():
                    newY = self.y + self.getSteps()
                else:
                    newY = self.y
                newX = self.x
            else:
                newX = self.x
                newY = self.y

        if (self.x != towardsX or self.y != towardsY) and self.gameWorld.isOccupied(towardsX, towardsY):
            defender = self.gameWorld.getOrganism(newX, newY)
            if defender is not None:
                self.collision(self, defender)

        self.gameWorld.moveOrganism(self.x, self.y, newX, newY)
