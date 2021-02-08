import re
from datetime import datetime, timedelta


from src.constants import Constants
from src.views import MainMenu
from src.models import Tournament, Players, Manager


class Controler:

    def __init__(self):
        self.menu = MainMenu()
        self.const = Constants()
        self.validator = Validator()
        self.db = Manager()
        self.tools = Tools()
        self.players_list = []

    def tournament_start_up(self):
        """
        Création d'un nouveau tournoi et création des 8 joueurs associés.
        :return:
        """
        self.menu.show_header(self.const.tournament_menu)
        if self.add_tournament():
            self.menu.show_header(self.const.new_player)
            if self.add_player():
                return True

    def start_tournament(self, index):
        """
        Chargement d'un tournoi et des joueurs associés au tournoi.
        :param index: ids du tournoi dans la db
        :return:
        """
        self.tourn = Tournament(*self.db.un_serialize_tournament(dict(self.db.load('tournament', index))))
        [self.tourn.players_inst.update({a[0]: Players(*a[1])}) for a in
         [(index, self.db.un_serialize_player(self.db.load("players", index))) for index in self.tourn.players_ids]]

    def add_tournament(self):
        """
        Création d'un tournoi.
        :return:
        """
        if self.get_infos('tournament_informations'):
            tourn_infos = [item['varname'] for item in self.const.tournament_informations]
            self.tourn = Tournament(name=tourn_infos[0], location=tourn_infos[1], start_date=tourn_infos[2],
                                    end_date=tourn_infos[3], nb_round=tourn_infos[4], r_time=tourn_infos[5],
                                    description=tourn_infos[6], players_ids=[], tournament_ids=0, players_inst={},
                                    rounds=[], matchs=[], finish=False)
            ids = self.db.save(self.tourn)
            self.tourn.tournament_ids = ids
        return True

    def add_player(self):
        """
        Création de 8 joueurs.
        :return:
        """
        for i in range(8):
            self.get_infos('players_informations')
            player = [item['varname'] for item in self.const.players_informations]
            player_infos = Players(first_name=player[0], last_name=player[1], b_date=player[2],
                                   sex=player[3], rank=player[4], score=0, player_ids=0, opponents=[],
                                   nickname=self.const.players_nickname[i])
            ids = self.db.save(player_infos)
            player_infos.player_ids = ids
            self.tourn.tournament_ids = ids

        return True

    def get_tournaments_from_db(self, index, finish):
        return [self.db.un_serialize_tournament(args) for args in
                self.db.load("tournament", index) if args['finish'] == finish]

    def get_players_from_db(self, index):
        """
        Chargement de joueurs depuis la db.
        :param index: all = tout les joeurs enregistré, int() joueur possédant l'id index.
        :return:
        """
        if index == "all":
            return [args for args in [self.db.un_serialize_player(self.db.load("players", "all"))]]
        else:
            return [args for args in [self.db.un_serialize_player(self.db.load("players", index)) for index in
                                      self.tourn.players_ids]]

    def get_players_from_inst(self, index):
        """
        Chargement de joueurs depuis self.tourn.players_inst (tournoi en cours).
        :param index: all = tout les joeurs enregistré, int() joueur possédant l'id index.
        :return: [['henry', 'titi', '30/08/1988', 'M', '85', 0, 9, [13], 'Joueur_1'],.....]
        """
        if index == "all":
            return [self.db.un_serialize_player(values) for values in
                                [player.__dict__ for player in [players for players in
                                                                self.tourn.players_inst.values()]]]
        else:
            return [player for player in self.tourn.players_inst[index].__dict__.values()]

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

    def get_countdown(self):
        """
        Chronomètre de round, si le temps est dépassé lancement de self.end_round().
        :return:
        """
        countdown = timedelta(minutes=int(self.tourn.r_time)) - \
                    (datetime.now() - datetime.strptime(self.tourn.rounds[-1][0][1], "%m/%d/%Y, %H:%M:%S"))
        r_time = timedelta(minutes=int(self.tourn.r_time))
        if r_time >= countdown:
            self.menu.show_countdown(((countdown.seconds % 3600) // 60), (countdown.seconds % 60))
        else:
            self.end_round()

    def play_round(self):
        """
        -----------------------NOT FINISH-----------------------------
        :return:
        """
        if len(self.tourn.rounds) == 0:
            first_pairs = self.get_first_pairs()
            self.update_opponents(first_pairs)
            self.menu.show_rounds("Lancement", self.const.round_name[len(self.tourn.rounds)])
            self.update_round(first_pairs)
            self.get_countdown()
        elif self.tourn.rounds[-1][0][2]:
            pairs = self.get_pairs()
            self.update_opponents(pairs)
            self.menu.show_rounds("Lancement", self.const.round_name[len(self.tourn.rounds)])
            self.update_round(pairs)
            self.get_countdown()
        else:
            return self.menu.show_rounds("Attendre la fin", self.tourn.rounds[-1][0][0])

    def end_round(self):
        """
        Fin de round: Ajout date/heure de fin et update de la db (tounoi en cours).
        :return:
        """
        self.tourn.rounds[-1][0][2] = self.tools.get_date()
        self.menu.show_rounds("Fin", self.const.round_name[len(self.tourn.rounds)-1])
        self.update_all(0)
        return True

    def get_first_pairs(self):
        """
        Calcul des paires du premier round.
        :return: [[<src.models.Players object at 0x000002515A9AB160>,...]
        """
        players_inst_list = [args[1] for args in self.tools.sort_by_rank(self.tourn.players_inst)]
        pairs_list = [[players_inst_list[i], players_inst_list[(len(players_inst_list)//2)+i]] for i in
                      range(len(players_inst_list) // 2)]
        return pairs_list

    def get_pairs(self):
        return [2]

    def update_opponents(self, pairs_list):
        """
        Enregistrement des adversaires affronté par chaque joueurs ( dans self.tourn.players_inst )
        :param pairs_list: [[<src.models.Players object at 0x000002515A9AB160>,...]
        :return:
        """
        for player in pairs_list:
            self.tourn.players_inst[player[0].player_ids].opponents.append(player[1].player_ids)
            self.tourn.players_inst[player[1].player_ids].opponents.append(player[0].player_ids)

    def update_round(self, pairs_list):
        """
        Implémentation de self.tourn.rounds.
        :param pairs_list: [[<src.models.Players object at 0x000002515A9AB160>,...]
        :return: [['Round_1', '02/08/2021, 08:23:44', False], [([8, 0], [4, 0]), ([7, 0], [3, 0]), ([6, 0], [2, 0]),
        ([5, 0], [1, 0])]]
        """
        self.tourn.rounds.append([[self.const.round_name[len(self.tourn.rounds)], self.tools.get_date(),
                                  False]])
        self.tourn.rounds[len(self.tourn.rounds) - 1].append([([player[0].player_ids, player[0].score],
                                                               [player[1].player_ids, player[1].score])
                                                              for player in pairs_list])

    def edit_player_score(self):
        self.menu.show_players(self.get_players_from_inst('all'))
        index = self.check_player_input(self.menu.get_input("Entrer le numéro du joueur", "à éditer", "EXEMPLE: 1\n\r"))
        self.menu.edit_player(self.get_players_from_inst(index), index)
        new_score = self.menu.get_new_score()
        if self.validator.is_positiv_float(new_score):
            self.tourn.players_inst[index].score += float(new_score)
        else:
            new_score = self.menu.get_new_score()
        return self.menu.edit_player(self.get_players_from_inst(index), index, "FINI!")

    def edit_player_rank(self):
        self.menu.show_players(self.get_players_from_inst('all'))
        index = self.check_player_input(self.menu.get_input("Entrer le numéro du joueur", "à éditer", "EXEMPLE: 1\n\r"))
        self.menu.edit_player(self.get_players_from_inst(index), index)
        new_rank = self.menu.get_new_rank()
        if self.validator.is_positiv_int(new_rank):
            self.tourn.players_inst[index].rank = new_rank
        else:
            new_rank = self.menu.get_new_rank()
        return self.menu.edit_player(self.get_players_from_inst(index), index, "FINI!")

    def update_all(self, index):
        """
        -----------------------------NOT WORKING-------------------------------
        :param index:
        :return:
        """
        self.db.update_all(self.tourn, index)

    def check_player_input(self, inp):
        """
        Vérifie que l'entrée de l'utilisateur corrspond bien à un joueur du tournoi.
        :param inp: user input
        :return: input
        """
        try:
            inp = int(inp)
            if inp in self.tourn.players_ids:
                return inp
        except ValueError as e:
            inp = self.menu.get_input(
                f'ERREUR: Vous avez entré {inp}, La réponse doit être un chiffre\n\r')
            self.check_player_input(inp)
        return False


class Tools:
    def __init__(self):
        pass

    def get_date(self):
        now = datetime.now()
        return now.strftime("%m/%d/%Y, %H:%M:%S")

    def sort_by_score(self, players):
        """
        :param players: Players {1: <src.models.Players object at 0x000001D666CB3310>,
                                 2: <src.models.Players object at 0x000001D666CB32E0>,......}
        :return:
        [(16, <src.models.Players object at 0x00000265A57AE700>),......)]
        """
        return sorted(players.items(), key=lambda x: int(getattr(x[1], 'score')), reverse=True)

    def sort_by_rank(self, players):
        """
        :param players: Players {1: <src.models.Players object at 0x000001D666CB3310>,
                                 2: <src.models.Players object at 0x000001D666CB32E0>,......}
        :return:
        [(16, <src.models.Players object at 0x00000265A57AE700>),......)]
        """
        return sorted(players.items(), key=lambda x: int(getattr(x[1], 'rank')), reverse=True)

    def sort_by_alpha(self, players):
        """
        :param players: Players {1: <src.models.Players object at 0x000001D666CB3310>,
                                 2: <src.models.Players object at 0x000001D666CB32E0>,......}
        :return:
        [(16, <src.models.Players object at 0x00000265A57AE700>),......)]
        """
        return sorted(players.items(), key=lambda x: getattr(x[1], 'first_name'), reverse=True)


class Validator:

    def is_alpha_sp(self, *args):
        p = re.compile(r'[a-zA-Z\s-]+')
        try:
            return all([True if len(re.search(p, arg)[0]) == len(arg) else False for arg in args])
        except TypeError as e:
            print(f'ERREUR: Valisator.is_alpha {e}')

    def is_printable(self, *args):
        p = re.compile(r'^[a-zA-Z.,;:\s-]+')
        try:
            return all([True if len(re.search(p, arg)[0]) == len(arg) else False for arg in args])
        except TypeError as e:
            print(f'ERREUR: Valisator.is_printable {e}')

    def is_date(self, *args):
        date_p = re.compile(r'^((\d\d\/){2}\d\d)')
        try:
            return all([True if re.match(date_p, arg) is not None else False for arg in args])
        except TypeError as e:
            print(f'ERREUR: Validator.is_date {e}')

    def is_sex(self, arg):
        return True if arg in ["M", "F"] else False

    def is_positiv_int(self, *args):
        try:
            [int(arg) for arg in list(args) if int(arg) >= 0]
            return True
        except TypeError as e:
            print(f'ERREUR: Validator.is_positiv_int {e}')
        except ValueError as e:
            print(f'ERREUR: Validator.is_positiv_int {e}')

    def is_positiv_float(self, *args):
        try:
            [float(arg) for arg in list(args) if float(arg) >= 0]
            return True
        except TypeError as e:
            print(f'ERREUR: Validator.is_positiv_float {e}')
        except ValueError as e:
            print(f'ERREUR: Validator.is_positiv_float {e}')


