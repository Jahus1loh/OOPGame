from Animal import Animal
from GameConstants import SQUARE_NUMBERS
from Commentator import Commentator


class Human(Animal):
    def __init__(self, strength, initiative, x, y, gameWorld):
        super().__init__(strength, initiative, x, y, gameWorld)
        self.last_key_pressed = ""
        self.special_ability_cd = 0

    def getName(self):
        return "Human"

    def getID(self):
        return 1

    def canUseSpecialAbility(self):
        return self.special_ability_cd == 0

    def getSpecialAbilityCD(self):
        return self.special_ability_cd

    def setSpecialAbilityCD(self, cd):
        self.special_ability_cd = cd

    def useSpecialAbility(self):
        if self.canUseSpecialAbility():
            organism = None
            humanX = self.getX()
            humanY = self.getY()
            dx = [-1, 1, 0, 0]
            dy = [0, 0, -1, 1]
            for i in range(4):
                organismX = humanX + dx[i]
                organismY = humanY + dy[i]
                if 0 <= organismX < SQUARE_NUMBERS and organismY < SQUARE_NUMBERS and self.gameWorld.isOccupied(
                        organismX, organismY) and organismY >= 0:
                    organism = self.gameWorld.getOrganism(organismX, organismY)
                    if organism is not None:
                        self.killOrganism(organism)

            self.setSpecialAbilityCD(5)
            Commentator.announceSpecialAbility()

    def move_left(self):
        newY = self.getY()
        x = self.getX()
        otherOrganism = None
        if newY > 0:
            newY -= 1
        otherOrganism = self.gameWorld.getOrganism(x, newY)
        if otherOrganism is not None:
            self.collision(self, otherOrganism)

        self.gameWorld.moveOrganism(x, self.getY(), x, newY)
        self.setY(newY)

    def move_right(self):
        newY = self.getY()
        x = self.getX()
        otherOrganism = None
        if newY > 0:
            newY += 1
        otherOrganism = self.gameWorld.getOrganism(x, newY)
        if otherOrganism is not None:
            self.collision(self, otherOrganism)

        self.gameWorld.moveOrganism(x, self.getY(), x, newY)
        self.setY(newY)

    def move_up(self):
        newX = self.getX()
        y = self.getY()
        otherOrganism = None
        if newX > 0:
            newX -= 1
        otherOrganism = self.gameWorld.getOrganism(newX, y)
        if otherOrganism is not None:
            self.collision(self, otherOrganism)

        self.gameWorld.moveOrganism(self.getX(), y, newX, y)
        self.setX(newX)

    def move_down(self):
        newX = self.getX()
        y = self.getY()
        otherOrganism = None
        if newX > 0:
            newX += 1
        otherOrganism = self.gameWorld.getOrganism(newX, y)
        if otherOrganism is not None:
            self.collision(self, otherOrganism)

        self.gameWorld.moveOrganism(self.getX(), y, newX, y)
        self.setX(newX)

    def set_last_key_pressed(self, key):
        self.last_key_pressed = key

    def action(self):
        direction = self.last_key_pressed
        if direction == "Up":
            self.move_up()
        elif direction == "Down":
            self.move_down()
        elif direction == "Left":
            self.move_left()
        elif direction == "Right":
            self.move_right()

        Commentator.announceMove(direction)
        self.last_key_pressed = ""
