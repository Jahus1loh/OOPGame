import tkinter as tk
from PIL import Image, ImageTk
from GameConstants import SQUARE_SIZE, NUMBER_OF_ORGANISMS, PERCENTAGE_TO_POPULATE, SQUARE_NUMBERS, HUMAN_STRENGTH, HUMAN_INITIATIVE, BELLADONNA_STRENGTH, GRASS_STRENGTH, GUARANA_STRENGTH, SOW_STRENGTH, SOSNOWSKY_STRENGTH, ANTELOPE_STRENGTH, ANTELOPE_INITIATIVE, FOX_STRENGTH, FOX_INITIATIVE, SHEEP_STRENGTH, SHEEP_INITIATIVE, TURTLE_STRENGTH, TURTLE_INITIATIVE, WOLF_STRENGTH, WOLF_INITIATIVE, PLANT_INITIATIVE, CYBER_SHEEP_STRENGTH, CYBER_SHEEP_INITIATIVE
from GameWorld import GameWorld
from Animals.Antelope import Antelope
from Animals.Fox import Fox
from Animals.Wolf import Wolf
from Animals.Turtle import Turtle
from Animals.Sheep import Sheep
from Plants.Belladonna import Belladonna
from Plants.Guarana import Guarana
from Plants.Grass import Grass
from Plants.Sosnowsky import Sosnowsky
from Plants.SowThistle import SowThistle
from Animals.CyberSheep import CyberSheep


class Board(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.boardArr = None
        self.buttons = [[None] * SQUARE_NUMBERS for _ in range(SQUARE_NUMBERS)]
        self.gameWorld = GameWorld()
        self.drawWorld()
        self.attachListeners()

    def drawWorld(self):
        self.boardArr = self.gameWorld.getWorld()
        for row in range(SQUARE_NUMBERS):
            for col in range(SQUARE_NUMBERS):
                filename = ""
                button = self.buttons[row][col] or tk.Button(self)
                button.config(borderwidth=1, relief="solid")

                if self.boardArr[row][col] == 0:
                    filename = "AnimalsImages/Blank.png"
                elif self.boardArr[row][col] == 1:
                    filename = "AnimalsImages/Human.png"
                elif self.boardArr[row][col] == 2:
                    filename = "AnimalsImages/Antelope.jpeg"
                elif self.boardArr[row][col] == 3:
                    filename = "AnimalsImages/Belladonna.png"
                elif self.boardArr[row][col] == 4:
                    filename = "AnimalsImages/Fox.png"
                elif self.boardArr[row][col] == 5:
                    filename = "AnimalsImages/Grass.png"
                elif self.boardArr[row][col] == 6:
                    filename = "AnimalsImages/Guarana.jpeg"
                elif self.boardArr[row][col] == 7:
                    filename = "AnimalsImages/Sheep.jpeg"
                elif self.boardArr[row][col] == 8:
                    filename = "AnimalsImages/Sosnowsky.jpeg"
                elif self.boardArr[row][col] == 9:
                    filename = "AnimalsImages/SowThistle.png"
                elif self.boardArr[row][col] == 10:
                    filename = "AnimalsImages/Turtle.jpeg"
                elif self.boardArr[row][col] == 11:
                    filename = "AnimalsImages/Wolf.jpeg"
                elif self.boardArr[row][col] == 12:
                    filename = "AnimalsImages/CyberSheep.jpeg"

                try:
                    image = Image.open(filename)
                    image = image.resize((SQUARE_SIZE, SQUARE_SIZE), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(image)
                    button.config(image=photo)
                    button.image = photo
                except IOError as ex:
                    print(f"Error loading {filename} image file: {ex}")

                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def attachListeners(self):
        for row in range(SQUARE_NUMBERS):
            for col in range(SQUARE_NUMBERS):
                button = self.buttons[row][col]
                buttonRow = row
                buttonCol = col
                button.config(command=lambda row=buttonRow, col=buttonCol: self.onButtonClicked(row, col))

    def onButtonClicked(self, row, col):
        if self.boardArr[row][col] == 0:
            print("1. {}".format(len(self.gameWorld.organismsOnBoard)))
            self.chooseOrganism(row, col)
            print("2. {}".format(len(self.gameWorld.organismsOnBoard)))
            self.drawWorld()

