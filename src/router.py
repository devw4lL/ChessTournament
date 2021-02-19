from src.views import MainMenu
from src.constants import Constants
from src.controlers import Controler
from src.utils import Tools


class Router:
    """
    La classe Router est une interface entre les views et le controlleur.
    """

    def __init__(self):
        self.menu = MainMenu()
        self.const = Constants()
        self.ctrl = Controler()
        self.tools = Tools()
        self.choice = ''
        self.tournament_running = False
        self.rounds_running = False

    def start_up(self):
        """
        Lancement du programme
        """
        self.menu.show_header(self.const.header, self.const.main_menu)
        self.check_input(self.menu.get_input("Veuillez entrer", "Le numéro de Menu: \n\r"))
        if self.choice == 1:  # Créer un nouveau tournoi
            self.ctrl.create_new_tournament_and_players()
            self.run_tournament()
        elif self.choice == 2:  # Reprendre un tournoi
            self.ctrl.resume_tournament()
            self.tournament_running = True
            self.run_rounds()
        elif self.choice == 3:  # Section rapport
            self.repport()  # <<<<<<--------------------------------------------------------------------
        elif self.choice == 4:  # Quit
            print("quit")
            self.exit()
        else:
            self.check_input(self.menu.get_input('', self.choice))

    def run_tournament(self):
        """
        Lancement du tournoi
        """
        self.tournament_running = True
        while True:
            self.menu.show_header(self.const.resume_menu)
            self.check_input(self.menu.get_input("Veuillez entrer", "Le numéro de Menu: \n\r"))
            if self.choice == 1:  # démarrer le nouveau tournoi
                self.ctrl.resume_tournament()
                self.ctrl.play_round()
            elif self.choice == 2:  # sauvgarder
                self.ctrl.tourn.update_all()
            elif self.choice == 3:  # menu précédent
                self.previous()
                self.start_up()
            else:
                self.check_input(self.menu.get_input('', self.choice))

    def run_rounds(self):
        """
        Lancement d'un round.
        """
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
                self.ctrl.tourn.update_all()
            elif self.choice == 7:  # menu précédent
                self.previous()
                self.run_tournament()

    def previous(self):
        """
        Gestion du passage à un menu précéfent, propose une sauvgarde si un tournoi est en cours.
        """
        if self.rounds_running or self.tournament_running:
            self.menu.show_header(self.const.quit_tournament)
            self.check_input(self.menu.get_input("Entrer le numéro correspondant: \n\r"))
            if self.choice == 1:
                self.ctrl.tourn.update_all()
        return True

    def repport(self):
        """
        Générateur de rapport.
        """
        while True:
            self.menu.show_header(self.const.report_menu)
            self.check_input(self.menu.get_input("Veuillez entrer", "Le numéro de Menu: \n\r"))
            if self.choice == 1:  # Tout les joueurs par ordre alphabétique.
                self.menu.show_players(self.tools.sort_by_alpha(self.ctrl.db.all_players())[::-1])
            elif self.choice == 2:  # Tout les joueurs par classement.
                self.menu.show_players(self.tools.sort_by_rank(self.ctrl.db.all_players()))
            elif self.choice == 3:  # Tout les tournois.
                self.menu.show_tournaments(self.ctrl.db.all_tournaments())
            elif self.choice == 4:  # Tout les joeurs d\'un tournoi par odre alphabétique.
                self.menu.show_players(self.tools.sort_by_rank([self.ctrl.db.get_player_from_db(ids)
                                                                for ids in
                                                                self.ctrl.get_specified_tournaments().players_ids])[
                                       ::-1])
            elif self.choice == 5:  # Tout les joeurs d\'un tournoi par classement.
                self.menu.show_players(self.tools.sort_by_alpha([self.ctrl.db.get_player_from_db(ids)
                                                                 for ids in
                                                                 self.ctrl.get_specified_tournaments().players_ids]))
            elif self.choice == 6:  # Tout les rounds d\'un tournoi.
                self.ctrl.get_specified_tournaments()
                self.menu.show_rounds(self.ctrl.parse_rounds()[1])
            elif self.choice == 7:  # Tout les matchs d\'un tournoi.
                self.ctrl.get_specified_tournaments()
                self.menu.show_matchs(self.ctrl.parse_rounds()[0])
            elif self.choice == 8:  # menu précédent
                self.previous()
                self.run_tournament()

    def check_input(self, inp):
        """
        Vérifie que l'entrée de l'utilisateur est un chiffre.
        :param inp: user input
        :return:
        """
        try:
            self.choice = int(inp)
        except ValueError as e:
            self.choice = self.menu.get_input(f'ERREUR {e}: Vous avez entré {inp}, '
                                              f'La réponse doit être un chiffre\n\r')
            self.check_input(self.choice)
        return True

    def exit(self):
        raise SystemExit
