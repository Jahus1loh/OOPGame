import pickle
import sys
import tkinter as tk
from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk

from GameConstants import *
import GameConstants
from GameWorld import GameWorld
from Animals.Antelope import Antelope
from Animals.Fox import Fox
from Animals.Wolf import Wolf
from Animals.Turtle import Turtle
from Animals.Sheep import Sheep
from Animals.Human import Human
from Animals.CyberSheep import CyberSheep
from Plants.Belladonna import Belladonna
from Plants.Guarana import Guarana
from Plants.Grass import Grass
from Plants.Sosnowsky import Sosnowsky
from Plants.SowThistle import SowThistle
from Commentator import Commentator


class MyFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.button_panel = None
        self.small_panel = None
        self.board_panel = None
        self.gameWorld = GameWorld(self)
        self.title("Jan Pastucha 193662")
        self.configure(bg=BACKGROUND)
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.resizable(False, False)
        self.bind_all("<Key>", self.handle_key_event)
        self.bind("<Left>", lambda event: self.handle_key_event("Left"))
        self.bind("<Right>", lambda event: self.handle_key_event("Right"))
        self.bind("<Up>", lambda event: self.handle_key_event("Up"))
        self.bind("<Down>", lambda event: self.handle_key_event("Down"))
        self.bind("<h>", lambda event: self.useAbility())
        self.columnconfigure(0, weight=300)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.small_panel = tk.Frame(self, bg=BACKGROUND)
        self.small_panel.grid(row=0, column=0)
        self.small_panel.columnconfigure(0, weight=100)
        self.small_panel.columnconfigure(SQUARE_NUMBERS + 2, weight=100)
        for i in range(SQUARE_NUMBERS):
            self.small_panel.columnconfigure(i + 1, weight=1)

        self.set_button_panel()

        self.boardArr = None
        self.buttons = [[None] * GameConstants.SQUARE_NUMBERS for _ in range(GameConstants.SQUARE_NUMBERS)]
        self.drawWorld()
        self.attachListeners()

    def set_button_panel(self):
        self.button_panel = tk.Frame(self, bg=BACKGROUND)
        self.button_panel.grid(column=0, row=SQUARE_NUMBERS + 2)
        self.button_panel.rowconfigure(0, weight=1)
        self.button_panel.rowconfigure(1, weight=1)
        self.button_panel.rowconfigure(2, weight=1)
        self.button_panel.columnconfigure(0, weight=10)
        for i in range(5):
            self.button_panel.columnconfigure(i + 1, weight=1)
        self.button_panel.columnconfigure(6, weight=10)

        exit_button = Button(self.button_panel, text="Exit", height=2, width=5, command=self.exit_application)
        save_button = tk.Button(self.button_panel, text="Save", height=2, width=5, command=self.saveGameState)
        restart_button = tk.Button(self.button_panel, text="Restart", height=2, width=5, command=self.resetGame)
        next_turn_button = tk.Button(self.button_panel, text="Next Turn", height=2, width=5, command=self.makeTurn)
        load_button = tk.Button(self.button_panel, text="Load", height=2, width=5, command=self.loadGameState)
        next_turn_button.grid(row=1, column=1)
        restart_button.grid(row=1, column=2)
        save_button.grid(row=1, column=3)
        load_button.grid(row=1, column=4)
        exit_button.grid(row=1, column=5)

    def resetGame(self):
        self.gameWorld = GameWorld(self)
        self.drawWorld()

    def exit_application(self):
        self.destroy()
        sys.exit(0)

    def makeTurn(self):
        self.gameWorld.makeTurn()
        self.drawWorld()
        Commentator.showLastEvents()
        Commentator.clearLastEvents()

    def handle_key_event(self, event):
        key = event.keysym
        human = self.gameWorld.getHuman()
        human.set_last_key_pressed(key)

    def useAbility(self):
        human = self.gameWorld.getHuman()
        human.useSpecialAbility()

    def drawWorld(self):
        self.boardArr = self.gameWorld.getWorld()
        for row in range(SQUARE_NUMBERS):
            for col in range(SQUARE_NUMBERS):
                filename = ""
                button = self.buttons[row][col] or tk.Button(self.small_panel)
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
                    image = image.resize((GameConstants.SQUARE_SIZE, GameConstants.SQUARE_SIZE), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(image)
                    button.config(image=photo)
                    button.image = photo
                except IOError as ex:
                    print(f"Error loading {filename} image file: {ex}")

                button.grid(row=row, column=col+1)
                self.buttons[row][col] = button

    def attachListeners(self):
        for row in range(GameConstants.SQUARE_NUMBERS):
            for col in range(GameConstants.SQUARE_NUMBERS):
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

    def chooseOrganism(self, x, y):
        organismNames = ["Antelope", "Belladonna", "CyberSheep", "Fox", "Grass", "Guarana", "Sheep", "Sosnowsky",
                         "SowThistle", "Turtle", "Wolf"]
        selectedOrganism = tk.StringVar()
        selectedOrganism.set(organismNames[0])

        def on_option_selected(selection):
            nonlocal selectedOrganism
            selectedOrganism.set(selection)

        def confirm_selection():
            selectedOrganismName = selectedOrganism.get()
            if selectedOrganismName is not None:
                selectedOrganismObject = None
                if selectedOrganismName == "Antelope":
                    selectedOrganismObject = Antelope(ANTELOPE_STRENGTH, ANTELOPE_INITIATIVE, x, y, self.gameWorld)
                elif selectedOrganismName == "Belladonna":
                    selectedOrganismObject = Belladonna(BELLADONNA_STRENGTH, PLANT_INITIATIVE, x, y, self.gameWorld)
                elif selectedOrganismName == "Fox":
                    selectedOrganismObject = Fox(FOX_STRENGTH, FOX_INITIATIVE, x, y, self.gameWorld)
                elif selectedOrganismName == "Grass":
                    selectedOrganismObject = Grass(GRASS_STRENGTH, PLANT_INITIATIVE, x, y, self.gameWorld)
                elif selectedOrganismName == "Guarana":
                    selectedOrganismObject = Guarana(GUARANA_STRENGTH, PLANT_INITIATIVE, x, y, self.gameWorld)
                elif selectedOrganismName == "Sheep":
                    selectedOrganismObject = Sheep(SHEEP_STRENGTH, SHEEP_INITIATIVE, x, y, self.gameWorld)
                elif selectedOrganismName == "Sosnowsky":
                    selectedOrganismObject = Sosnowsky(SOSNOWSKY_STRENGTH, PLANT_INITIATIVE, x, y, self.gameWorld)
                elif selectedOrganismName == "SowThistle":
                    selectedOrganismObject = SowThistle(SOW_STRENGTH, PLANT_INITIATIVE, x, y, self.gameWorld)
                elif selectedOrganismName == "Turtle":
                    selectedOrganismObject = Turtle(TURTLE_STRENGTH, TURTLE_INITIATIVE, x, y, self.gameWorld)
                elif selectedOrganismName == "Wolf":
                    selectedOrganismObject = Wolf(WOLF_STRENGTH, WOLF_INITIATIVE, x, y, self.gameWorld)
                elif selectedOrganismName == "CyberSheep":
                    selectedOrganismObject = CyberSheep(CYBER_SHEEP_STRENGTH, CYBER_SHEEP_INITIATIVE, x, y,
                                                        self.gameWorld)
                if selectedOrganismObject:
                    self.gameWorld.addOrganismToList(selectedOrganismObject)
                    self.drawWorld()
                    root.destroy()

        root = tk.Toplevel(self)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        popup_width = int(screen_width / 4)
        popup_height = int(screen_height / 4)
        popup_x = int((screen_width - popup_width) / 2)
        popup_y = int((screen_height - popup_height) / 2)
        root.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        organismMenu = tk.OptionMenu(root, selectedOrganism, *organismNames, command=on_option_selected)
        organismMenu.pack()

        confirmButton = tk.Button(root, text="Confirm", command=confirm_selection)
        confirmButton.pack()


    def saveGameState(self):
        filePath = filedialog.askopenfilename()
        if filePath:
            try:
                gameData = {}

                # Save the turn number
                gameData['turnNumber'] = self.gameWorld.getTurnNumber()

                # Save the human ability cooldown
                human = self.gameWorld.getHuman()
                gameData['humanAbilityCD'] = human.getSpecialAbilityCD()

                # Save the organisms
                organisms = self.gameWorld.getOrganismsOnBoard()
                organisms_data = []

                for organism in organisms:
                    if organism:
                        organism_data = {
                            'name': organism.getName(),
                            'strength': organism.getStrength(),
                            'initiative': organism.getInitiative(),
                            'x': organism.getX(),
                            'y': organism.getY(),
                            'age': organism.getAge()
                        }
                        organisms_data.append(organism_data)

                gameData['organisms'] = organisms_data

                with open(filePath, 'wb') as file:
                    pickle.dump(gameData, file)

                print("Game saved successfully.")

            except IOError as ex:
                print("Error saving game:", ex)

    def loadGameState(self):
        filePath = filedialog.askopenfilename()
        if filePath:
            try:
                with open(filePath, 'rb') as file:
                    gameState = pickle.load(file)
                    self.gameWorld.clearWorld()

                    turnNumber = gameState['turnNumber']
                    self.gameWorld.setTurnNumber(turnNumber)

                    organisms = gameState['organisms']
                    organisms_list = []
                    for organismData in organisms:
                        name = organismData['name']
                        strength = organismData['strength']
                        initiative = organismData['initiative']
                        x = organismData['x']
                        y = organismData['y']
                        age = organismData['age']

                        organism = self.createOrganism(name, strength, initiative, x, y)
                        organism.setAge(age)

                        organisms_list.append(organism)

                    self.gameWorld.setOrganisms(organisms_list)
                    humanAbilityCD = gameState['humanAbilityCD']
                    human = self.gameWorld.getHuman()
                    human.setSpecialAbilityCD(humanAbilityCD)

            except (IOError, pickle.PickleError) as ex:
                print("Error loading game state: ", ex)

        self.drawWorld()

    def createOrganism(self, name, strength, initiative, x, y):
        organism = None
        if name == "Human":
            organism = Human(strength, initiative, x, y, self)
        elif name == "Antelope":
            organism = Antelope(strength, initiative, x, y, self)
        elif name == "Belladonna":
            organism = Belladonna(strength, initiative, x, y, self)
        elif name == "Fox":
            organism = Fox(strength, initiative, x, y, self)
        elif name == "Grass":
            organism = Grass(strength, initiative, x, y, self)
        elif name == "Guarana":
            organism = Guarana(strength, initiative, x, y, self)
        elif name == "Sheep":
            organism = Sheep(strength, initiative, x, y, self)
        elif name == "Sosnowsky":
            organism = Sosnowsky(strength, initiative, x, y, self)
        elif name == "SowThistle":
            organism = SowThistle(strength, initiative, x, y, self)
        elif name == "Turtle":
            organism = Turtle(strength, initiative, x, y, self)
        elif name == "Wolf":
            organism = Wolf(strength, initiative, x, y, self)

        if organism is not None:
            self.gameWorld.addOrganismToWorld(organism)

        return organism
