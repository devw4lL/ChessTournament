import re
from datetime import datetime, timedelta
from pprint import pprint


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

    def resume_tournament(self, index):
        """
        Chargement d'un tournoi commencé et non fini.
        :param index:
        :return:
        """
        self.tourn = Tournament(*self.db.un_serialize_tournament(dict(self.db.load('tournament', index))))
        for player in self.get_players_from_db(self.tourn.players_inst):
            self.tourn.players_inst.append(Players(*player))
            self.tourn.players_inst.pop(0)

    def add_tournament(self):
        """
        Création d'un tournoi.
        :return:
        """
        if self.get_infos('tournament_informations'):
            tourn_infos = [item['varname'] for item in self.const.tournament_informations]
            self.tourn = Tournament(name=tourn_infos[0], location=tourn_infos[1], start_date=tourn_infos[2],
                                    end_date=tourn_infos[3], nb_round=tourn_infos[4], r_time=tourn_infos[5],
                                    description=tourn_infos[6], players_ids=[], tournament_ids=0, players_inst=[],
                                    rounds=[], matchs=[], finish=False)
            ids = self.db.save(self.tourn)
            self.tourn.tournament_ids = ids
        self.update_tournament(self.tourn.tournament_ids)
        return True

    def add_player(self):
        """
        Création de 8 joueurs.
        :return:
        """
        for i in range(1):  # Attention remettre 8
            self.get_infos('players_informations')
            player = [item['varname'] for item in self.const.players_informations]
            player_infos = Players(first_name=player[0], last_name=player[1], b_date=player[2],
                                   sex=player[3], rank=player[4], score=0, player_ids=0, opponents=[],
                                   nickname=self.const.players_nickname[i])
            ids = self.db.save(player_infos)
            player_infos.player_ids = ids
            self.tourn.players_inst.append(ids)
            self.tourn.players_ids.append(ids)
        self.update_tournament(self.tourn.tournament_ids)
        return True

    def get_tournaments_from_db(self, index, finish=True):
        if index == 'all':
            return [self.db.un_serialize_tournament(args) for args in
                    self.db.load("tournament", index) if args['finish'] == finish]
        else:
            return [self.db.un_serialize_tournament(dict(self.db.load("tournament", index)))]

    def get_players_from_db(self, index):
        """
        Chargement de joueurs depuis la db.
        :param index: all = tout les joeurs enregistrés, int() joueur possédant l'id index.
        :return: [['al', 'fred', '14/06/1988', 'M', '12', 0, 1, [], 'Joueur_1'],..........]
        """
        if index == "all":
            return [args for args in [self.db.un_serialize_player(self.db.load("players", "all"))]]
        else:
            return [args for args in [self.db.un_serialize_player(self.db.load("players", index)) for index in
                                      self.tourn.players_ids]]

    def get_players_from_inst_ids(self, index):
        """
        Chargement des joueurs depuis self.tourn.players_inst (tournoi en cours).
        Transforme les players_ids en list d'infos.
        :param index: all = tout les joeurs enregistré, int() joueur possédant l'id index.
        :return: [['henry', 'titi', '30/08/1988', 'M', '85', 0, 9, [13], 'Joueur_1'],.....]
        """
        if index == "all":
            return [[getattr(p, k) for (k, v) in self.const.player.items()] for p in
                    [player for player in [players for players in self.tourn.players_inst]]]
        else:
            return [getattr(self.tourn.players_inst[index], k) for (k, v) in self.const.player.items()]

    def get_players_ids_from_inst(self):
        return [player.player_ids for player in self.tourn.players_inst]


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
        if len(self.tourn.rounds) == 0:  # 1er round
            first_pairs = self.get_first_pairs()
            self.update_opponents(first_pairs)
            self.menu.show_rounds("Lancement", self.const.round_name[len(self.tourn.rounds)])
            self.update_round(first_pairs)
            self.get_countdown()
        elif len(self.tourn.rounds) < int(self.tourn.nb_round):
            if self.tourn.rounds[-1][0][2]:  # 2éme round j'usqu'a nb_round
                pairs = self.get_pairs()
                self.update_opponents(pairs)
                self.menu.show_rounds("Lancement", self.const.round_name[len(self.tourn.rounds)])
                self.update_round(pairs)
                self.get_countdown()
            else:
                self.menu.show_rounds("Attendre la fin", self.tourn.rounds[-1][0][0])
        else:
            return False
        return True

    def end_round(self):
        """
        Fin de round: Ajout date/heure de fin et update de la db (tounoi en cours).
        :return:
        ------------------------NOT WORKING---------------------------
        """
        self.tourn.rounds[-1][0][2] = self.tools.get_date()
        self.menu.show_rounds("Fin", self.const.round_name[len(self.tourn.rounds)-1])
        return False

    def get_first_pairs(self):
        """
        Calcul des paires du premier round.
        :return: [[<src.models.Players object at 0x0000021BC9B4EF70>,
                    <src.models.Players object at 0x0000021BC9C28AC0>],.....]
        """
        players_inst_list = self.tools.sort_by_rank(self.tourn.players_inst)
        pairs_list = [[players_inst_list[i], players_inst_list[(len(players_inst_list)//2)+i]] for i in
                      range(len(players_inst_list) // 2)]
        [self.menu.show_pairs([[v for k, v in pair[0].__dict__.items()], [v for k, v in pair[1].__dict__.items()]],
                              i + 1) for i, pair in enumerate(pairs_list)]
        print("pair_list", pairs_list)
        return pairs_list

    def get_pairs(self):
        """
        Calcul des paires du deuxième round et suivant.
        :return: [[<src.models.Players object at 0x0000021BC9B4EF70>,
                    <src.models.Players object at 0x0000021BC9C28AC0>],.....]
        """
        print("p-score", self.tourn.players_inst)
        p_by_score = self.tools.sort_by_score(self.tourn.players_inst)
        potential_pairs, opponents_pairs, final_pairs = [], [], []
        while len(opponents_pairs) != len(p_by_score):
            potential_pairs.append(self.tools.compare_score_and_rank(p_by_score[0], p_by_score[1]))
            opponents_pairs.append(self.tools.compare_by_opponents(potential_pairs, p_by_score))
            tmp = [f for p in opponents_pairs for f in p]
            [p_by_score.remove(player) for player in tmp if player in p_by_score]
            final_pairs.append(*opponents_pairs)
            potential_pairs.clear(), opponents_pairs.clear()
        [self.menu.show_pairs([[v for k, v in pair[0].__dict__.items()], [v for k, v in pair[1].__dict__.items()]],
                              i + 1) for i, pair in enumerate(final_pairs)]
        print("final_pairs", final_pairs)
        return final_pairs

    def update_opponents(self, pairs_list):
        """
        Enregistrement des adversaires affrontés par chaque joueur ( dans self.tourn.players_inst )
        :param pairs_list: [[<src.models.Players object at 0x000002515A9AB160>,...]
        :return:
        """
        for player in pairs_list:
            player[0].opponents.append(player[1].player_ids)
            player[1].opponents.append(player[0].player_ids)

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
        self.menu.show_players(self.get_players_from_inst_ids('all'))
        index = self.check_player_input(self.menu.get_input("Entrer le numéro du joueur", "à éditer", "EXEMPLE: 1\n\r"))
        self.menu.edit_player(self.get_players_from_inst_ids(index - 1), index - 1)
        new_score = self.menu.get_new_score()
        if self.validator.is_positiv_float(new_score):
            self.tourn.players_inst[index].score += float(new_score)
        else:
            new_score = self.menu.get_new_score()
        return self.menu.edit_player(self.get_players_from_inst_ids(index), index, "FINI!")

    def edit_player_rank(self):
        self.menu.show_players(self.get_players_from_inst_ids('all'))
        index = self.check_player_input(self.menu.get_input("Entrer le numéro du joueur", "à éditer", "EXEMPLE: 1\n\r"))
        self.menu.edit_player(self.get_players_from_inst_ids(index - 1), index - 1)
        new_rank = self.menu.get_new_rank()
        if self.validator.is_positiv_int(new_rank):
            self.tourn.players_inst[index].rank = new_rank
        else:
            new_rank = self.menu.get_new_rank()
        return self.menu.edit_player(self.get_players_from_inst_ids(index), index, "FINI!")

    def update_tournament(self, tourn_index):
        self.db.update_all(self.tourn, tourn_index)
        return True

    def update_all(self, tourn_index):
        """
        -----------------------------NOT WORKING-------------------------------
        :param index:
        :return:
        """
        print("update_all_controller", tourn_index)
        print(self.tourn.players_inst)
        self.tourn.players_inst = self.get_players_ids_from_inst()
        print(self.tourn.players_inst)
        if tourn_index:
            self.db.update_all(self.tourn, tourn_index)
            for player in self.tourn.players_inst:
                self.db.update_all(player, player.player_ids)

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
            print(f'ERREUR: check_player_input')

        return self.check_player_input( self.menu.get_input(
                f'ERREUR: Vous avez entré {inp}, Le chiffre doit correspondre à un joueur!\n\r'))


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
        return sorted(players, key=lambda x: int(getattr(x, 'score')))

    def sort_by_rank(self, players):
        """
        :param players: Players {1: <src.models.Players object at 0x000001D666CB3310>,
                                 2: <src.models.Players object at 0x000001D666CB32E0>,......}
        :return:
        [(16, <src.models.Players object at 0x00000265A57AE700>),......)]
        """
        return sorted(players, key=lambda x: int(getattr(x, 'rank')), reverse=True)

    def sort_by_alpha(self, players):
        """
        :param players: Players {1: <src.models.Players object at 0x000001D666CB3310>,
                                 2: <src.models.Players object at 0x000001D666CB32E0>,......}
        :return:
        [(16, <src.models.Players object at 0x00000265A57AE700>),......)]
        """
        return sorted(players, key=lambda x: getattr(x, 'first_name'), reverse=True)

    def compare_score_and_rank(self, player_one, player_two):
        if player_one.score == player_two.score:
            if player_one.rank >= player_two.rank:
                return [player_one, player_two]
        return [player_two, player_one]

    def compare_by_opponents(self, potential_pairs, p_by_score):
        if potential_pairs[0][0].player_ids in potential_pairs[0][1].opponents:
            for i in range(1, len(p_by_score)-1):
                if not potential_pairs[0][0].player_ids in p_by_score[i+1].opponents:
                    return [potential_pairs[0][0], p_by_score[i+1]]
        return [potential_pairs[0][0], potential_pairs[0][1]]


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


