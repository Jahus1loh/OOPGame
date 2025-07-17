import random
from Animal import Animal
from Commentator import Commentator
import GameConstants


class Fox(Animal):
    def __init__(self, strength, initiative, x, y, gameWorld):
        super().__init__(strength, initiative, x, y, gameWorld)
        self.gameWorld = gameWorld

    def getName(self):
        return "Fox"

    def getID(self):
        return 4

    def action(self):
        random_num = random.randint(1, 4)
        new_x = 0
        new_y = 0

        if random_num == 1:
            if self.x > self.getSteps() - 1:
                new_x = self.x - self.getSteps()
            else:
                new_x = self.x
            new_y = self.y
        elif random_num == 2:
            if self.y > self.getSteps() - 1:
                new_y = self.y - self.getSteps()
            else:
                new_y = self.y
            new_x = self.x
        elif random_num == 3:
            if self.x < GameConstants.SQUARE_NUMBERS - self.getSteps():
                new_x = self.x + self.getSteps()
            else:
                new_x = self.x
            new_y = self.y
        elif random_num == 4:
            if self.y < GameConstants.SQUARE_NUMBERS - self.getSteps():
                new_y = self.y + self.getSteps()
            else:
                new_y = self.y
            new_x = self.x
        else:
            new_x = self.x
            new_y = self.y

        if (self.x != new_x or self.y != new_y) and self.gameWorld.isOccupied(new_x, new_y):
            defender = self.gameWorld.getOrganism(new_x, new_y)
            if defender:
                if defender.getStrength() <= self.getStrength():
                    self.collision(self, defender)
                else:
                    Commentator.announceFear(self)
                    new_x = self.x
                    new_y = self.y

        print(f"Organism moved from {self.x} {self.y} to position {new_x} {new_y}")
        self.gameWorld.moveOrganism(self.x, self.y, new_x, new_y)
        self.setX(new_x)
        self.setY(new_y)
