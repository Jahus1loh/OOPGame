import tkinter as tk
from tkinter import messagebox


class Commentator:
    lastEvents = ""

    def __init__(self):
        pass

    @staticmethod
    def getInstance():
        return Commentator()

    @staticmethod
    def announceFight(attacker, defender):
        Commentator.getInstance().appendText(attacker.getName() + " attacked the " + defender.getName())

    @staticmethod
    def announceDeath(victim):
        Commentator.getInstance().appendText(victim.getName() + " has been killed")

    @staticmethod
    def announceBreeding(animal):
        Commentator.getInstance().appendText(animal.getName() + " bred")

    @staticmethod
    def announceEscape(organism):
        Commentator.getInstance().appendText(organism.getName() + " escaped from a fight")

    def announceFear(organism):
        Commentator.getInstance().appendText(organism.getName() + " feared a fight and stayed in the same place")

    @staticmethod
    def announceEatingOfGuarana(organism):
        Commentator.getInstance().appendText(
            organism.getName() + " ate Guarana plant and increased its strength by 3, now it's " + str(
                organism.getStrength()))

    @staticmethod
    def announceSpecialAbility():
        Commentator.getInstance().appendText("Human used their special ability")

    @staticmethod
    def announceSawing(organism):
        Commentator.getInstance().appendText(organism.getName() + " saw a plant")

    @staticmethod
    def announceMove(direction):
        Commentator.getInstance().appendText("Human moved {}".format(direction))
        print("Human moved {}".format(direction))

    def appendText(self, text):
        Commentator.lastEvents += text + "\n"

    @staticmethod
    def showLastEvents():
        messagebox.showinfo("Last Turn Events", Commentator.lastEvents)

    @staticmethod
    def clearLastEvents():
        Commentator.lastEvents = ""
