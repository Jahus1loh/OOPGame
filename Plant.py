import random
import GameConstants
from GameConstants import SQUARE_NUMBERS, NUMBER_OF_ORGANISMS, CHANCE_TO_SAW, BELLADONNA_STRENGTH, GRASS_STRENGTH, GUARANA_STRENGTH
from Organism import Organism
from Commentator import Commentator


class Plant(Organism):
    def init(self, strength, initiative, x, y, gameWorld):
        super().__init__(strength, initiative, x, y, gameWorld)
        self.rand = random.Random()
        self.gameWorld = gameWorld

    @staticmethod
    def inBounds(x, y):
        return 0 <= x < SQUARE_NUMBERS and 0 <= y < SQUARE_NUMBERS

    def getName(self):
        return None

    def escape(self):
        return False

    def isPlant(self):
        return True

    def action(self):
        randomNumber = self.rand.randint(2, NUMBER_OF_ORGANISMS + 1)

        if randomNumber < CHANCE_TO_SAW * 100:
            newPlant = None
            plantX = self.x
            plantY = self.y
            plantId = self.getID()
            dx = [-1, 1, 0, 0]
            dy = [0, 0, -1, 1]
            indices = []

            for i in range(4):
                x = plantX + dx[i]
                y = plantY + dy[i]

                if self.inBounds(x, y) and not self.gameWorld.isOccupied(x, y):
                    indices.append(i)

            if indices:
                randomIndex = self.rand.choice(indices)
                newX = plantX + dx[randomIndex]
                newY = plantY + dy[randomIndex]

                if plantId == 3:
                    newPlant = self.gameWorld.createOrganism("Belladona", newX, newY)
                elif plantId == 5:
                    newPlant = self.gameWorld.createOrganism("Grass", newX, newY)
                elif plantId == 6:
                    newPlant = self.gameWorld.createOrganism("Guarana", newX, newY)
                elif plantId == 8:
                    newPlant = self.gameWorld.createOrganism("Sosnowsky", newX, newY)
                elif plantId == 9:
                    newPlant = self.gameWorld.createOrganism("SowThistle", newX, newY)

                if newPlant:
                    self.gameWorld.addOrganismToList(newPlant)
                    Commentator.announceSawing(newPlant)

