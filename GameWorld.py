from tkinter import messagebox
import random
import math
from GameConstants import NUMBER_OF_ORGANISMS, PERCENTAGE_TO_POPULATE, SQUARE_NUMBERS, HUMAN_STRENGTH, HUMAN_INITIATIVE, BELLADONNA_STRENGTH, GRASS_STRENGTH, GUARANA_STRENGTH, SOW_STRENGTH, SOSNOWSKY_STRENGTH, ANTELOPE_STRENGTH, ANTELOPE_INITIATIVE, FOX_STRENGTH, FOX_INITIATIVE, SHEEP_STRENGTH, SHEEP_INITIATIVE, TURTLE_STRENGTH, TURTLE_INITIATIVE, WOLF_STRENGTH, WOLF_INITIATIVE, PLANT_INITIATIVE, CYBER_SHEEP_STRENGTH, CYBER_SHEEP_INITIATIVE
from Animals.Antelope import Antelope
from Animals.Fox import Fox
from Animals.Wolf import Wolf
from Animals.Turtle import Turtle
from Animals.Sheep import Sheep
from Animals.Human import Human
from Plants.Belladonna import Belladonna
from Plants.Guarana import Guarana
from Plants.Grass import Grass
from Plants.Sosnowsky import Sosnowsky
from Plants.SowThistle import SowThistle
from Animals.CyberSheep import CyberSheep


class GameWorld:
    def __init__(self, window):
        self.rand = random.Random()
        self.turnNumber = 0
        self.organismCount = 0
        self.organismsOnBoard = []
        self.board = [[0] * SQUARE_NUMBERS for _ in range(SQUARE_NUMBERS)]
        self.window = window
        self.populateWorld()

    def getWorld(self):
        return self.board

    def getOrganismsOnBoard(self):
        return self.organismsOnBoard

    def getTurnNumber(self):
        return self.turnNumber

    def setTurnNumber(self, turnNumber):
        self.turnNumber = turnNumber

    def setOrganisms(self, organisms):
        self.organismsOnBoard = organisms

    def getOrganismsCount(self):
        return self.organismCount

    def generateHuman(self, x, y):
        organism = Human(HUMAN_STRENGTH, HUMAN_INITIATIVE, x, y, self)
        self.board[x][y] = 1
        self.organismsOnBoard.append(organism)
        self.organismCount += 1

    def generateOrganism(self, x, y):
        organism = None
        organismNumber = self.rand.randint(2, NUMBER_OF_ORGANISMS + 1)
        if organismNumber == 2:
            organism = Antelope(ANTELOPE_STRENGTH, ANTELOPE_INITIATIVE, x, y, self)
        elif organismNumber == 3:
            organism = Belladonna(BELLADONNA_STRENGTH, PLANT_INITIATIVE, x, y, self)
        elif organismNumber == 4:
            organism = Fox(FOX_STRENGTH, FOX_INITIATIVE, x, y, self)
        elif organismNumber == 5:
            organism = Grass(GRASS_STRENGTH, PLANT_INITIATIVE, x, y, self)
        elif organismNumber == 6:
            organism = Guarana(GUARANA_STRENGTH, PLANT_INITIATIVE, x, y, self)
        elif organismNumber == 7:
            organism = Sheep(SHEEP_STRENGTH, SHEEP_INITIATIVE, x, y, self)
        elif organismNumber == 8:
            organism = Sosnowsky(SOSNOWSKY_STRENGTH, PLANT_INITIATIVE, x, y, self)
        elif organismNumber == 9:
            organism = SowThistle(SOW_STRENGTH, PLANT_INITIATIVE, x, y, self)
        elif organismNumber == 10:
            organism = Turtle(TURTLE_STRENGTH, TURTLE_INITIATIVE, x, y, self)
        elif organismNumber == 11:
            organism = Wolf(WOLF_STRENGTH, WOLF_INITIATIVE, x, y, self)
        elif organismNumber == 12:
            organism = CyberSheep(CYBER_SHEEP_STRENGTH, CYBER_SHEEP_INITIATIVE, x, y, self)

        if organism is not None:
            self.board[x][y] = organismNumber
            self.organismsOnBoard.append(organism)
            self.organismCount += 1

    def populateWorld(self):
        numberOfCellsToOccupy = PERCENTAGE_TO_POPULATE * math.pow(SQUARE_NUMBERS, 2)
        for _ in range(int(numberOfCellsToOccupy)):
            x = self.rand.randint(0, SQUARE_NUMBERS - 1)
            y = self.rand.randint(0, SQUARE_NUMBERS - 1)
            while self.isOccupied(x, y):
                x = self.rand.randint(0, SQUARE_NUMBERS - 1)
                y = self.rand.randint(0, SQUARE_NUMBERS - 1)
            self.generateOrganism(x, y)

        x = self.rand.randint(0, SQUARE_NUMBERS - 1)
        y = self.rand.randint(0, SQUARE_NUMBERS - 1)
        while self.isOccupied(x, y):
            x = self.rand.randint(0, SQUARE_NUMBERS - 1)
            y = self.rand.randint(0, SQUARE_NUMBERS - 1)
        self.generateHuman(x, y)

    @staticmethod
    def inBounds(x, y):
        return 0 <= x < SQUARE_NUMBERS and 0 <= y < SQUARE_NUMBERS

    def isOccupied(self, x, y):
        return self.board[x][y] != 0

    def moveOrganism(self, oldx, oldY, newX, newY):
        if oldx != newX or oldY != newY:
            self.board[newX][newY] = self.board[oldx][oldY]
            self.board[oldx][oldY] = 0

    def removeOrganism(self, organism):
        self.board[organism.getX()][organism.getY()] = 0

        index = -1
        for i in range(len(self.organismsOnBoard)):
            if self.organismsOnBoard[i] == organism:
                index = i
                break

        if index >= 0:
            newOrganismsOnBoard = []
            for i in range(len(self.organismsOnBoard)):
                if i != index:
                    newOrganismsOnBoard.append(self.organismsOnBoard[i])
            self.organismsOnBoard = newOrganismsOnBoard
            self.organismCount -= 1

    def getOrganism(self, x, y):
        for organism in self.organismsOnBoard:
            if organism is not None and organism.getX() == x and organism.getY() == y:
                return organism
        return None

    def determineMoveOrder(self):
        nonNullOrganisms = [organism for organism in self.organismsOnBoard if organism is not None]
        self.organismsOnBoard = sorted(nonNullOrganisms, key=lambda x: (x.getInitiative(), -x.getAge()), reverse=True)
        for organism in self.organismsOnBoard:
            self.board[organism.getX()][organism.getY()] = organism.getID()

    def humanAlive(self):
        for organism in self.organismsOnBoard:
            if organism is not None and organism.getName() == "Human":
                return True
        return False

    def makeTurn(self):
        print("Trying to make turn")
        self.determineMoveOrder()
        if not self.humanAlive():
            result = messagebox.showerror("Game Over", "You died!")
            if result == "ok":
                exit(0)
        for organism in self.organismsOnBoard:
            if organism is not None:
                currentX = organism.getX()
                currentY = organism.getY()
                if self.inBounds(currentX, currentY):
                    organism.action()
                    organism.setAge(organism.getAge() + 1)
        self.turnNumber += 1
        print("Made turn")

    def getHuman(self):
        for organism in self.organismsOnBoard:
            if organism is not None and organism.getName() == "Human":
                return organism
        return None

    def addOrganismToList(self, organism):
        self.board[organism.getX()][organism.getY()] = organism.getID()
        self.organismsOnBoard.append(organism)
        self.organismCount += 1

    def addOrganismToWorld(self, organism):
        self.board[organism.getX()][organism.getY()] = organism.getID()

    def createOrganism(self, name, x, y):
        organism = None
        if name == "Human":
            organism = Human(HUMAN_STRENGTH, HUMAN_INITIATIVE, x, y, self)
        elif name == "Antelope":
            organism = Antelope(ANTELOPE_STRENGTH, ANTELOPE_INITIATIVE, x, y, self)
        elif name == "Belladonna":
            organism = Belladonna(BELLADONNA_STRENGTH, PLANT_INITIATIVE, x, y, self)
        elif name == "Fox":
            organism = Fox(FOX_STRENGTH, FOX_INITIATIVE, x, y, self)
        elif name == "Grass":
            organism = Grass(GRASS_STRENGTH, PLANT_INITIATIVE, x, y, self)
        elif name == "Guarana":
            organism = Guarana(GUARANA_STRENGTH, PLANT_INITIATIVE, x, y, self)
        elif name == "Sheep":
            organism = Sheep(SHEEP_STRENGTH, SHEEP_INITIATIVE, x, y, self)
        elif name == "Sosnowsky":
            organism = Sosnowsky(SOSNOWSKY_STRENGTH, PLANT_INITIATIVE, x, y, self)
        elif name == "SowThistle":
            organism = SowThistle(SOW_STRENGTH, PLANT_INITIATIVE, x, y, self)
        elif name == "Turtle":
            organism = Turtle(TURTLE_STRENGTH, TURTLE_INITIATIVE, x, y, self)
        elif name == "Wolf":
            organism = Wolf(WOLF_STRENGTH, WOLF_INITIATIVE, x, y, self)
        elif name == "CyberSheep":
            organism = CyberSheep(CYBER_SHEEP_STRENGTH, CYBER_SHEEP_INITIATIVE, x, y, self)

        if organism is not None:
            self.addOrganismToWorld(organism)

    def clearWorld(self):
        for i in range(SQUARE_NUMBERS):
            for j in range(SQUARE_NUMBERS):
                self.board[i][j] = 0
        for i in range(len(self.organismsOnBoard)):
            self.organismsOnBoard[i] = None
