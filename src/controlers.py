from datetime import datetime, timedelta

from src.constants import Constants
from src.models import Manager
from src.modules.utils import Tools
from src.modules.validator import Validator
from src.modules.run_tournaments import RunTournaments
from src.views import MainMenu


class Controler:
    """
    La classe Controler gère la creation et le déroulement des tournois.
    """

    def __init__(self):
        self.menu = MainMenu()
        self.const = Constants()
        self.validator = Validator()
        self.tools = Tools()
        self.db = Manager()
        self.tourn = RunTournaments()
        self.report = None
        self.players_list = []

    def create_new_tournament_and_players(self):
        """
        Création d'un nouveau tournoi et création des 8 joueurs associés.
        :return: int: ids du tounoi créer.
        """
        self.menu.show_header(self.const.tournament_menu)
        if self.get_infos('tournament_informations'):
            tourn_infos = [item['varname'] for item in self.const.tournament_informations]
            self.tourn.add_tournament(tourn_infos)
            self.menu.show_header(self.const.new_player)
            for i in range(1):
                if self.get_infos('players_informations'):
                    player = [item['varname'] for item in self.const.players_informations]
                    self.tourn.add_player(player, i)
        self.menu.show_tournaments([self.db.get_tournament_from_db(self.tourn.current_tourn.tournament_ids)],
                                   'Vous avec correctement ajouter le tournoi: \n\r')
        self.menu.show_infos("Contenant les joueurs: \n\r")
        self.menu.show_players([self.db.get_player_from_db(ids) for ids in
                                self.db.get_tournament_from_db(self.tourn.current_tourn.tournament_ids).players_ids])
        return self.tourn.current_tourn.tournament_ids

    def resume_tournament(self):
        """
        Reprise d'un tournoi déjà enregistré dans la db.
        :return: int: ids du en cours.
        """
        self.menu.show_tournaments(self.db.get_tournaments_by_status(finish=False))
        self.tourn.reload_tourn(self.check_tournament_ids(self.menu.get_input('Entrer le numéro du tournoi'
                                                                              ' à reprendre.', 'EXEMPLE:', '2')))
        self.tourn.reload_players()
        self.menu.show_infos(f'Vous venez de charger le tounoi: {self.tourn.current_tourn.tournament_ids}\n\r'
                             f'Contenant les joueurs : \n\r')
        self.menu.show_players(self.tourn.current_tourn.players_inst)

        return self.tourn.current_tourn.tournament_ids

    def get_infos(self, mode):
        """
        Récupère les infos pour la création de joueurs et de tournois et vérifie les informations entrée.
        :param mode: player --> ajout de joueurs, tournament --> ajout de tournois.
        :return:
        """
        for item in getattr(self.const, mode):
            item['varname'] = self.menu.get_input(item['description'])
            for validator in item['validator']:
                while not getattr(Validator(), validator)(item['varname']):
                    item['varname'] = self.menu.get_input(item['description'])
        return True

    def play_round(self):
        """
        Gestionnaire de rounds et de matchs
        :return: bool: status du tournoi, False = Fin de tournoi.
        """
        if len(self.tourn.current_tourn.rounds) == 0:  # 1er round
            self.tourn.get_first_pairs()
            [self.menu.show_pairs(pair, index=num + 1) for num, pair in enumerate(self.tourn.current_pairs)]
            self.tourn.update_opponents()
            self.menu.show_rounds_status("Lancement", self.const.round_name[len(self.tourn.current_tourn.rounds)])
            self.tourn.update_round()
            self.get_countdown()
        elif len(self.tourn.current_tourn.rounds) < int(self.tourn.current_tourn.nb_round):
            if self.tourn.current_tourn.rounds[-1][0][2]:  # 2éme round j'usqu'a nb_round
                self.tourn.get_pairs()
                [self.menu.show_pairs(pair, index=num + 1) for num, pair in enumerate(self.tourn.current_pairs)]
                self.tourn.update_opponents()
                self.menu.show_rounds_status("Lancement", self.const.round_name[len(self.tourn.current_tourn.rounds)])
                self.tourn.update_round()
                self.get_countdown()
            else:
                self.menu.show_rounds_status("Attendre la fin", self.tourn.current_tourn.rounds[-1][0][0])
        else:
            self.menu.show_infos(self.const.end_tournament)
            return False
        return True

    def end_round(self):
        """
        Fin de round: Ajout date/heure de fin et update de la db (tounoi en cours).
        :return: bool: status du round, False = round fini ou tournoi fini.
        """
        if len(self.tourn.current_tourn.rounds) != int(self.tourn.current_tourn.nb_round):
            self.menu.show_rounds_status("Fin", self.const.round_name[len(self.tourn.current_tourn.rounds) - 1])
            self.tourn.update_round(finish=True)
            self.tourn.update_all()
            self.tourn.reload_players()
            self.edit_player_score()
            return False
        self.menu.show_infos(self.const.end_tournament)
        self.edit_player_rank()
        self.tourn.update_all()
        return False

    def edit_player_score(self):
        self.menu.show_players(self.tourn.current_tourn.players_inst)
        ids = self.check_player_input(
            self.menu.get_input("Entrer le numéro du joueur", "à éditer", "EXEMPLE: 1\n\r"))
        self.menu.show_infos(f'EDITION DU JOUEUR: {ids} !!')
        new_score = self.menu.get_input("Entrer le nouveau", "score", "EXEMPLE: 1")
        if self.validator.is_positiv_float(new_score):
            if self.tourn.edit_score(ids, new_score):
                self.menu.show_infos(f'FIN D\'EDITION DU JOUEUR: {ids} !!\n\r')
        else:
            self.menu.show_infos(f'ERREUR: Le score doit être possitif (saisie:{new_score}).')
        return True

    def edit_player_rank(self):
        self.menu.show_players(self.tourn.current_tourn.players_inst)
        ids = self.check_player_input(
            self.menu.get_input("Entrer le numéro du joueur", "à éditer", "EXEMPLE: 1\n\r"))
        self.menu.show_infos(f'EDITION DU JOUEUR: {ids} !!')
        new_rank = self.menu.get_input("Entrer le nouveau", "Classement", "EXEMPLE: 1")
        if self.validator.is_positiv_float(new_rank):
            if self.tourn.edit_rank(ids, new_rank):
                self.menu.show_infos(f'FIN D\'EDITION DU JOUEUR: {ids} !!\n\r')
        else:
            self.menu.show_infos(f'ERREUR: Le Classement doit être un entier possitif (saisie:{new_rank}).')
        return True

    def get_countdown(self):
        """
        Chronomètre de round, si le temps est dépassé lancement de self.end_round().
        """
        countdown = timedelta(minutes=int(self.tourn.current_tourn.r_time)) - (datetime.now() -
                                                                               datetime.strptime(
                                                                                   self.tourn.current_tourn.rounds[-1][
                                                                                       0][1],
                                                                                   "%m/%d/%Y, %H:%M:%S"))
        r_time = timedelta(minutes=int(self.tourn.current_tourn.r_time))
        if r_time >= countdown:
            self.menu.show_countdown(((countdown.seconds % 3600) // 60), (countdown.seconds % 60))
        else:
            self.menu.show_infos(f'Fin du round: {self.tourn.current_tourn.rounds[-1][0][0]}.'
                                 f'\n\rLe temps imparti de {self.tourn.current_tourn.r_time} est écoulé.')
            self.end_round()

    def get_specified_tournaments(self):
        """
        Créer une instance de tournoi différente pour la génération de rapport.
        :return: obj: Instance Tounament.
        """
        self.menu.show_tournaments(self.db.all_tournaments())
        self.report = self.db.get_tournament_from_db(
            self.check_tournament_ids(self.menu.get_input('Entrer le numéro du tournoi.', 'EXEMPLE:', '2')))
        return self.report

    def parse_rounds(self):
        """
        Sépare les rounds et les matchs, détermine qui est le gagnant entre chaque matchs.
        :param tournament: obj: Instance Tournament généré par get_specified_tournaments().
        :return: list: de tout les rounds et list: de tout les matchs.
        """
        all_rounds, all_matchs = [], []
        for rounds in self.report.rounds:
            all_rounds.append(rounds[0])
            for i, matchs in enumerate(rounds[1]):
                j1_ids, j1_s, j2_ids, j2_s = matchs[0][0], matchs[0][1], matchs[1][0], matchs[1][1]
                if j1_s < j2_s:
                    all_matchs.append([i + 1, j2_ids, j2_s, j1_ids, j1_s, rounds[0][0]])
                elif j1_s == j2_s:
                    all_matchs.append([i + 1, j2_ids, j2_s, j1_ids, j1_s, rounds[0][0]])
                else:
                    all_matchs.append([i + 1, j1_ids, j1_s, j2_ids, j2_s, rounds[0][0]])
        return all_matchs, all_rounds

    def check_player_input(self, inp):
        """
        Vérifie que l'entrée de l'utilisateur correspond bien à un joueur du tournoi.
        :param inp: user input
        :return: input
        """
        try:
            inp = int(inp)
            if inp in self.tourn.current_tourn.players_ids:
                return inp
        except ValueError as e:
            print(f'ERREUR {e}: check_player_input')

        return self.check_player_input(self.menu.get_input(
            f'ERREUR: Vous avez entré {inp}, Le chiffre doit correspondre à un joueur!\n\r'))

    def check_tournament_ids(self, inp):
        """
        Vérifie que l'entrée de l'utilisateur corrspond bien à un tournoi dans la db.
        :param inp: user input
        :return: input si l'ids existe, sinon False
        """
        try:
            inp = int(inp)
            if inp in range(len(self.db.tournaments_db) + 1):
                return inp
        except ValueError as e:
            print(f'ERREUR{e}: check_tournament_ids')
        return False
