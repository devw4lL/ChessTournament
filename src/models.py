import os

from tinydb import TinyDB
from src.constants import Constants
from src.modules.tournament import Tournament
from src.modules.players import Players


class Manager:
    """
    Manadger des bases de données tournaments_db & players_db.
    """

    def __init__(self):
        self.const = Constants()
        self.db_path = TinyDB(os.path.join(os.path.dirname(__file__), "db", "db.json"))
        self.players_db = self.db_path.table('players')
        self.tournaments_db = self.db_path.table('tournaments')

    def save(self, obj):
        if obj.__class__.__name__ == "Players":
            ids = self.players_db.insert({k: getattr(obj, k) for (k, v) in self.const.player.items()})
            return ids
        elif obj.__class__.__name__ == "Tournament":
            ids = self.tournaments_db.insert({k: getattr(obj, k) for (k, v) in self.const.tournament.items()})
            return ids

    def update(self, obj, index):
        if obj.__class__.__name__ == "Players":
            for k, v in obj.__dict__.items():
                self.players_db.update({k: getattr(obj, k)}, doc_ids=[index])
            return True
        elif obj.__class__.__name__ == "Tournament":
            for k, v in obj.__dict__.items():
                self.tournaments_db.update({k: getattr(obj, k)}, doc_ids=[index])
            return True

    def load(self, db, index=0):
        if db == "Tournament":
            if not index:
                return [self.get_tournament_from_db(all_tourn['tournament_ids']) for all_tourn in
                        self.tournaments_db.all()]
            return self.tournaments_db.get(doc_id=index)

        elif db == "Player":
            if not index:
                return [self.get_player_from_db(players_ids['player_ids']) for players_ids in self.players_db.all()]
            return self.players_db.get(doc_id=index)
        return False

    def get_player_from_db(self, index=0):
        """
        Récupére les informations du joueur à l'index donnée et renvoi une instance de la class Players.
        :param index: int (ids d'un player dans la players_db).
        :return: Instance d'un player.
        """
        player_infos = [values for keys, values in self.load("Player", index).items()]
        return Players(*player_infos)

    def get_tournament_from_db(self, index=0):
        """
        Récupére les informations du tournoi à l'index donnée dans la db.
        :param index: int (ids d'un tournoi dans tournaments_db ).
        :return: Instance d'un tournoi.
        """
        tournament_infos = [values for keys, values in self.load("Tournament", index).items()]
        return Tournament(*tournament_infos)

    def all_tournaments(self):
        """
        :return: Instances de tout les tournois dans la db.
        """
        return [tournament for tournament in self.load('Tournament')]

    def get_tournaments_by_status(self, finish=False):
        """
        :param finish: True = tournoi fini, False = tournoi non fini.
        :return: Instances de tout les tournois dans la db  en fonction de son status.
        """
        return [tournament for tournament in self.load('Tournament') if tournament.finish == finish]

    def all_players(self):
        """
        :return: Instances de tout les joueurs de le db.
        """
        return [players for players in self.load('Player')]
