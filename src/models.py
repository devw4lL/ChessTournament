import os

from tinydb import TinyDB, Query
from src.constants import Constants
from src.utils import Tools

# ----------Database init----------------------------------------------------
db_path = TinyDB(os.path.join(os.path.dirname(__file__), "db", "db.json"))
players_db = db_path.table('players')
tournaments_db = db_path.table('tournaments')


# -----------------------------------------------------------------------------


class Tournament:
    def __init__(self, name, location, start_date, end_date, nb_round, r_time, description, players_ids,
                 tournament_ids, players_inst, rounds, finish):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.nb_round = nb_round
        self.r_time = r_time
        self.description = description
        self.players_ids = players_ids
        self.tournament_ids = tournament_ids
        self.players_inst = players_inst
        self.rounds = rounds
        self.finish = finish

    def save_tournament(self):
        self.players_inst.clear()
        return Manager().save(self)  # Return db ids of new Tournament.

    def update_tournament(self):
        self.clear_players_inst()
        return Manager().update(self, self.tournament_ids)

    def clear_players_inst(self):
        self.players_inst.clear()
        return True

    def update_all_players(self):
        try:
            for player in self.players_inst:
                player.update_player()
        except ValueError as e:
            print(f'Erreur dans src.models.Tournament {e}')


class Players:
    def __init__(self, first_name, last_name, b_date, sex, rank, score, player_ids, opponents, nickname):
        self.first_name = first_name
        self.last_name = last_name
        self.b_date = b_date
        self.sex = sex
        self.rank = rank
        self.score = score
        self.player_ids = player_ids
        self.opponents = opponents
        self.nickname = nickname

    def save_player(self):
        return Manager().save(self)  # Return db ids of new Player.

    def update_player(self):
        return Manager().update(self, self.player_ids)


class RunTournaments:
    """
    Reprise d'un tournoi précédement enregistré et/ou non fini
    """

    def __init__(self):
        self.db = Manager()
        self.const = Constants()
        self.tools = Tools()
        self.current_pairs = []
        self.current_tourn = None
        self.player = None

    def add_tournament(self, tourn_infos):
        """
        Création d'un tournoi.
        :return:
        """
        self.current_tourn = Tournament(name=tourn_infos[0], location=tourn_infos[1], start_date=tourn_infos[2],
                                        end_date=tourn_infos[3], nb_round=tourn_infos[4], r_time=tourn_infos[5],
                                        description=tourn_infos[6], players_ids=[], tournament_ids=0, players_inst=[],
                                        rounds=[], finish=False)
        ids = self.current_tourn.save_tournament()
        self.current_tourn.tournament_ids = int(ids)
        self.current_tourn.update_tournament()
        return True

    def add_player(self, player_infos, nickname_id):
        """
        Création de 8 joueurs.
        :return:
        """
        self.player = Players(first_name=player_infos[0], last_name=player_infos[1], b_date=player_infos[2],
                              sex=player_infos[3], rank=int(player_infos[4]), score=0, player_ids=0, opponents=[],
                              nickname=self.const.players_nickname[nickname_id])
        ids = self.player.save_player()
        self.player.player_ids = int(ids)
        self.player.update_player()
        self.current_tourn.players_ids.append(int(ids))
        self.current_tourn.update_tournament()
        return True

    def reload_tourn(self, index):
        """
        Chargement d'un tournoi commencé et non fini.
        :param index: Ids du tournoi à reprendre.
        :return:
        """
        self.current_tourn = self.db.get_tournament_from_db(
            self.db.load('Tournament', int(index))['tournament_ids'])
        return True

    def reload_players(self):
        """
        Chargement des joueurs du tournoi depuis la DB
        :return: implémentation de self.tourn.players_inst
        """
        for ids in self.current_tourn.players_ids:
            self.current_tourn.players_inst.append(self.db.get_player_from_db(ids))

    def get_first_pairs(self):
        """
        Calcul des paires du premier round.
        :return: [[<src.models.Players object at 0x0000021BC9B4EF70>,
                    <src.models.Players object at 0x0000021BC9C28AC0>],.....]
        """
        if not self.current_tourn.players_inst:
            self.reload_players()
        players_inst_list = self.tools.sort_by_rank(self.current_tourn.players_inst)
        self.current_pairs = [[players_inst_list[i], players_inst_list[(len(players_inst_list) // 2) + i]] for i in
                              range(len(players_inst_list) // 2)]
        return True

    def get_pairs(self):
        """
        Calcul des paires du deuxième round et suivant.
        :return: [[<src.models.Players object at 0x0000021BC9B4EF70>,
                    <src.models.Players object at 0x0000021BC9C28AC0>],.....]
        """
        if not self.current_tourn.players_inst:
            self.reload_players()
        p_by_score = self.tools.sort_by_score(self.current_tourn.players_inst)
        potential_pairs, opponents_pairs, final_pairs = [], [], []
        while len(opponents_pairs) != len(p_by_score):
            potential_pairs.append(self.tools.compare_score_and_rank(p_by_score[0], p_by_score[1]))
            opponents_pairs.append(self.tools.compare_by_opponents(potential_pairs, p_by_score))
            tmp = [f for p in opponents_pairs for f in p]
            [p_by_score.remove(player) for player in tmp if player in p_by_score]
            self.current_pairs.append(*opponents_pairs)
            potential_pairs.clear(), opponents_pairs.clear()
        return True

    def update_opponents(self):
        """
        Enregistrement des adversaires affrontés par chaque joueur ( dans self.tourn.players_inst )
        :param pairs_list: [[<src.models.Players object at 0x000002515A9AB160>,...]
        :return:
        """
        for player in self.current_pairs:
            p1 = self.current_tourn.players_inst.index(player[0])
            p2 = self.current_tourn.players_inst.index(player[1])
            self.current_tourn.players_inst[p1].opponents.append(player[1].player_ids)
            self.current_tourn.players_inst[p2].opponents.append(player[0].player_ids)
            # player[0].opponents.append(player[1].player_ids)  # pour les pairs en cours
            # player[1].opponents.append(player[0].player_ids)  # pour les pairs en cours
        self.current_tourn.update_all_players()
        return True

    def update_round(self, finish=False):
        """
        Implémentation de self.tourn.rounds.
        :param pairs_list: [[<src.models.Players object at 0x000002515A9AB160>,...]
        :return: [['Round_1', '02/08/2021, 08:23:44', False], [([8, 0], [4, 0]), ([7, 0], [3, 0]), ([6, 0], [2, 0]),
        ([5, 0], [1, 0])]]
        """
        if not finish:
            self.current_tourn.rounds.append(
                [[self.const.round_name[len(self.current_tourn.rounds)], self.tools.get_date(),
                  False]])
            self.current_tourn.rounds[len(self.current_tourn.rounds) - 1].append(
                [([player[0].player_ids, player[0].score],
                  [player[1].player_ids, player[1].score])
                 for player in self.current_pairs])
            return True
        self.current_tourn.rounds[-1][0][2] = self.tools.get_date()
        self.current_pairs.clear()
        return True

    def edit_score(self, ids, new_score):
        [setattr(player, 'score', (player.score + float(new_score)))
         for player in self.current_tourn.players_inst if getattr(player, 'player_ids') == ids]
        return True

    def edit_rank(self, ids, new_rank):
        [setattr(player, 'rank', (player.rank + new_rank))
         for player in self.current_tourn.players_inst if getattr(player, 'player_ids') == ids]
        return True


class Manager:

    def __init__(self):
        self.const = Constants()

    def save(self, obj):
        if obj.__class__.__name__ == "Players":
            ids = players_db.insert({k: getattr(obj, k) for (k, v) in self.const.player.items()})
            return ids
        elif obj.__class__.__name__ == "Tournament":
            ids = tournaments_db.insert({k: getattr(obj, k) for (k, v) in self.const.tournament.items()})
            return ids

    def update(self, obj, index):
        if obj.__class__.__name__ == "Players":
            # print("update_players ", obj, index)
            for k, v in obj.__dict__.items():
                # print("---------------", k, v)
                players_db.update({k: getattr(obj, k)}, doc_ids=[index])
            return True
        elif obj.__class__.__name__ == "Tournament":
            # print("update_tournament", obj, index)
            for k, v in obj.__dict__.items():
                # print("---------------", k, v)
                tournaments_db.update({k: getattr(obj, k)}, doc_ids=[index])
            return True

    def load(self, db, index=0):
        if db == "Tournament":
            if not index:
                return [self.get_tournament_from_db(all_tourn['tournament_ids']) for all_tourn in tournaments_db.all()]
            # print("load")
            return tournaments_db.get(doc_id=index)

        elif db == "Player":
            if not index:
                # print("db_load_all_player", players_db.all())
                return [self.get_player_from_db(players_ids['player_ids']) for players_ids in players_db.all()]
            return players_db.get(doc_id=index)
        return False

    def get_player_from_db(self, index=0):
        """
        Récupére les informations du joueur à l'index donnée et renvoi une instance de la class Players
        :param index: int (ids d'un player dans la players_db)
        :return: Instance d'un player.
        """
        player_infos = [values for keys, values in self.load("Player", index).items()]
        return Players(*player_infos)

    def get_tournament_from_db(self, index=0):
        """
        Récupére les informations du tournoi à l'index donnée dans la db.
        :param index: int (ids d'un tournoi dans tournaments_db )
        :return: Instance d'un tournoi.
        """
        tournament_infos = [values for keys, values in self.load("Tournament", index).items()]
        return Tournament(*tournament_infos)

    def all_tournaments(self, finish=False):
        return [tournament for tournament in self.load('Tournament') if not finish]

    def all_players(self):
        return [players for players in self.load('Player')]

    def un_serialize_tournament(self, tournaments):
        """
        -------------Renvoi des instances !!!!!!!
        :param tournaments:
        :return:
        """
        # print("serialize_tourn", tournaments, type(tournaments))
        return [values for keys, values in tournaments.items()]

    def un_serialize_player(self, players):
        """
        -------------Renvoi des instances !!!!!!!
        :param players: {'first_name': 'al', 'last_name': 'fred', 'b_date': '14/06/1988', 'sex': 'M',
                          'rank': '12', 'score': 0, 'player_ids': 1, 'opponents': [], 'nickname': 'Joueur_1'}
        :return: ['al', 'fred', '14/06/1988', 'M', '12', 0, 1, [], 'Joueur_1']
        """
        # print("serialize_players", players)
        return [values for keys, values in players.items()]


if __name__ == '__main__':
    M = Manager()

    print(M.get_tournament_from_db(1))
