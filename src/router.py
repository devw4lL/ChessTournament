import re
import threading

from src.views import MainMenu
from src.constants import Constants
from src.controlers import Controler


class Router:

    def __init__(self):
        self.menu = MainMenu()
        self.const = Constants()
        self.ctrl = Controler()
        self.choice = ''
        self.tournament_running = False
        self.rounds_running = False

    def start_up(self):
        self.menu.show_header(self.const.header, self.const.main_menu)
        self.check_input(self.menu.get_input("Veuillez entrer", "Le numéro de Menu: \n\r"))
        if self.choice == 1:  # Créer un nouveau tournoi
            self.run_tournament(self.ctrl.create_new_tournament_and_players())
        elif self.choice == 2:  # Reprendre un tournoi
            self.ctrl.resume_tournament()
            self.tournament_running = True
            self.run_rounds()
        elif self.choice == 3:  # Section rapport
            self.repport()
        elif self.choice == 4:  # Quit
            print("quit")
            self.exit()
        else:
            self.check_input(self.menu.get_input('', self.choice))

    def run_tournament(self, index):
        self.tournament_running = True
        while True:
            self.menu.show_header(self.const.resume_menu)
            self.check_input(self.menu.get_input("Veuillez entrer", "Le numéro de Menu: \n\r"))
            if self.choice == 1:  # démarrer le nouveau tournoi
                self.ctrl.resume_tournament()
                self.ctrl.play_round()
            elif self.choice == 2:  # sauvgarder
                self.ctrl.update_all()
            elif self.choice == 3:  # menu précédent
                self.start_up()
            else:
                self.check_input(self.menu.get_input('', self.choice))

    def run_rounds(self):
        while self.tournament_running:
            self.menu.show_header(self.const.round_menu)
            self.check_input(self.menu.get_input("Veuillez entrer", "Le numéro de Menu: \n\r"))
            if self.choice == 1:  # chronomètre
                self.ctrl.get_countdown()
            elif self.choice == 2:  # lancer round
                self.tournament_running = self.ctrl.play_round()
                self.rounds_running = True
            elif self.choice == 3:  # cloturer round
                self.rounds_running = self.ctrl.end_round()
            elif self.choice == 4:  # editer score joueur
                self.ctrl.edit_player_score()
            elif self.choice == 5:  # editer classement d'un joueur
                self.ctrl.edit_player_rank()
            elif self.choice == 6:  # sauvgarder
                self.ctrl.update_all()
            elif self.choice == 7:  # menu précédent
                #------------------- demandé si sauvgarder car le tournoi est en cours -----------------
                self.run_tournament(-1)

    def repport(self):
        pass

    def check_input(self, inp):
        """
        Vérifie que l'entrée de l'utilisateur est un chiffre.
        :param inp: user input
        :return:
        """
        try:
            self.choice = int(inp)
        except ValueError as e:
            self.choice = self.menu.get_input(f'ERREUR: Vous avez entré {inp}, La réponse doit être un chiffre\n\r')
            self.check_input(self.choice)
        return True

    def exit(self):
        raise SystemExit
