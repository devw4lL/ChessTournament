from src.constants import Constants
from src.models import Manager
from src.modules.utils import Tools
from src.modules.players import Players
from src.modules.tournament import Tournament


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
        self.player = Players(first_name=player_infos[0].title(), last_name=player_infos[1], b_date=player_infos[2],
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
        return True

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
        potential_pairs, opponents_pairs = [], []
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
        """
        for player in self.current_pairs:
            p1 = self.current_tourn.players_inst.index(player[0])
            p2 = self.current_tourn.players_inst.index(player[1])
            self.current_tourn.players_inst[p1].opponents.append(player[1].player_ids)
            self.current_tourn.players_inst[p2].opponents.append(player[0].player_ids)
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

    def update_all(self):
        self.current_tourn.update_tournament()
        self.current_tourn.update_all_players()
        return True

    def edit_score(self, ids, new_score):
        [setattr(player, 'score', (player.score + float(new_score)))
         for player in self.current_tourn.players_inst if getattr(player, 'player_ids') == ids]
        return True

    def edit_rank(self, ids, new_rank):
        [setattr(player, 'rank', (player.rank + int(new_rank)))
         for player in self.current_tourn.players_inst if getattr(player, 'player_ids') == ids]
        return True
