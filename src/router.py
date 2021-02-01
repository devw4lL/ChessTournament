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
        if self.choice == 1:
            if self.ctrl.tournament_start_up():
                self.tournament_run(-1)
        elif self.choice == 2:
            self.menu.show_tournaments(self.ctrl.get_tournaments("all", finish=False))
            index = self.check_input(self.menu.get_input("\n\rVeuillez entrer", "Le numéro du tournoi à reprendre: ",
                                                         "\n\r"))
            self.tournament_run(index)
        elif self.choice == 3:
            self.repport()
        elif self.choice == 4:
            self.exit()
        else:
            self.check_input(self.menu.get_input('', self.choice))

    def tournament_run(self, index):
        self.tournament_running = True
        while True:
            self.menu.show_header(self.const.resume_menu)
            self.check_input(self.menu.get_input("Veuillez entrer", "Le numéro de Menu: \n\r"))
            if self.choice == 1: #démarrer tournoi
                self.ctrl.start_tournament(index)
                self.rounds_run()
            elif self.choice == 6:  # sauvgarder
                self.ctrl.save_all()
            elif self.choice == 7:  # menu précédent
                self.start_up()
            else:
                self.check_input(self.menu.get_input('', self.choice))

    def rounds_run(self):
        self.rounds_running = True
        while self.tournament_running and self.rounds_running:
            self.menu.show_header(self.const.round_menu)
            self.check_input(self.menu.get_input("Veuillez entrer", "Le numéro de Menu: \n\r"))
            if self.choice == 1:  # chronomètre
                countdown = threading.Thread(self.ctrl.get_countdown(self.ctrl.tourn.r_time, True),
                                             self.menu.get_input('Appuyer sur echap pour quiter le chornometre.'))
                countdown.start()
                countdown.join()
                chr(27)
                self.ctrl.get_countdown(self.ctrl.tourn.r_time, False)

            elif self.choice == 2:  # lancer round
                self.ctrl.play_round()

            elif self.choice == 3:  # cloturer round
                self.ctrl.end_round()

            elif self.choice == 4:  # editer score joueur
                self.menu.show_players(self.ctrl.get_players(-1))
                self.ctrl.edit_player_score(self.check_input(self.menu.get_input("Veuillez entrer", "Le numéro du "
                                                                                                    "joueur: \n\r")))
            elif self.choice == 5:  # editer classement d'un joueur
                self.menu.show_players(self.ctrl.get_players(0))
                self.ctrl.edit_player_rank()

            elif self.choice == 6:  # sauvgarder
                self.ctrl.save_all()

            elif self.choice == 7:  # menu précédent
                self.tournament_run(-1)

    def repport(self):
        pass

    def check_input(self, inp):
        try:
            self.choice = int(inp)
        except ValueError as e:
            self.choice = self.menu.get_input(f'ERREUR: Vous avez entré {inp}, La réponse doit être un chiffre\n\r')
            self.check_input(self.choice)
        return True

    def exit(self):
        raise SystemExit
