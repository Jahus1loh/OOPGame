from abc import ABC, abstractmethod
from random import randint, shuffle
from tkinter import messagebox
from Commentator import Commentator
from GameConstants import SQUARE_NUMBERS


class Organism(ABC):
    def __init__(self, strength, initiative, x, y, gameWorld):
        self.strength = strength
        self.initiative = initiative
        self.x = x
        self.y = y
        self.gameWorld = gameWorld
        self.age = 0

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def escape(self):
        pass

    @abstractmethod
    def isPlant(self):
        pass

    def getStrength(self):
        return self.strength

    def getInitiative(self):
        return self.initiative

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getAge(self):
        return self.age

    def getOrganism(self):
        return self

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setStrength(self, strength):
        self.strength = strength

    def setInitiative(self, initiative):
        self.initiative = initiative

    def setAge(self, age):
        self.age = age

    def getID(self):
        return 0

    def collision(self, attacker, defender):
        escape = randint(0, 1)
        if self.sameSpecies(attacker, defender):
            self.breedAnimals(attacker)
        if attacker.getName() == "CyberSheep" and defender.getName() == "Sosnowsky":
            self.killOrganism(defender)
        if defender.getName() == "Turtle" and attacker.getStrength() < 5:
            self.killOrganism(attacker)
        elif defender.getName() == "Belladonna" or defender.getName() == "Sosnowsky":
            self.killOrganism(attacker)
        elif defender.getName() == "Guarana":
            attacker.setStrength(attacker.getStrength() + 3)
            Commentator.announceEatingOfGuarana(attacker)
        else:
            Commentator.announceFight(attacker, defender)
            if attacker.getStrength() > defender.getStrength():
                if defender.getName() == "Antelope" and escape == 0:
                    Commentator.announceEscape(defender)
                else:
                    self.killOrganism(defender)
                    Commentator.announceDeath(defender)
            elif attacker.getStrength() < defender.getStrength():
                if attacker.getName() == "Antelope" and escape == 0:
                    Commentator.announceEscape(attacker)
                else:
                    self.killOrganism(attacker)
                    Commentator.announceDeath(attacker)
            else:
                if attacker.getAge() > defender.getAge():
                    self.killOrganism(defender)
                    Commentator.announceDeath(defender)
                else:
                    self.killOrganism(attacker)
                    Commentator.announceDeath(attacker)

    def sameSpecies(self, attacker, defender):
        defenderName = defender.getName()
        attackerName = attacker.getName()
        return defenderName == attackerName

    def killOrganism(self, organism):
        if organism.getName() == "Human":
            messagebox.showerror("Game Over", "You died!")
            exit(0)
        self.gameWorld.removeOrganism(organism)

    def use_special_ability(self):
        pass

    def set_last_key_pressed(self, key):
        pass

    @staticmethod
    def inBounds(x, y):
        return 0 <= x < SQUARE_NUMBERS and 0 <= y < SQUARE_NUMBERS

    def breedAnimals(self, animal):
        newAnimal = None
        animalX = animal.getX()
        animalY = animal.getY()
        animalID = animal.getID()
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        indices = []

        for i in range(4):
            x = animalX + dx[i]
            y = animalY + dy[i]
            if self.inBounds(x, y) and not self.gameWorld.isOccupied(x, y):
                indices.append(i)

        shuffle(indices)

        newX = animalX + dx[indices[0]]
        newY = animalY + dy[indices[0]]

        if animalID == 2:
            newAnimal = self.gameWorld.createOrganism("Antelope", newX, newY)
        elif animalID == 4:
            newAnimal = self.gameWorld.createOrganism("Fox", newX, newY)
        elif animalID == 7:
            newAnimal = self.gameWorld.createOrganism("Sheep", newX, newY)
        elif animalID == 10:
            newAnimal = self.gameWorld.createOrganism("Turtle", newX, newY)
        elif animalID == 11:
            newAnimal = self.gameWorld.createOrganism("Wolf", newX, newY)
        elif animalID == 12:
            newAnimal = self.gameWorld.createOrganism("CyberSheep", newX, newY)

        if newAnimal is not None:
            self.gameWorld.addOrganismToList(newAnimal)
            Commentator.announceBreeding(newAnimal)