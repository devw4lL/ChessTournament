import os
from pprint import pprint

from tinydb import TinyDB, Query
from src.constants import Constants

# ----------Database init----------------------------------------------------
db_path = TinyDB(os.path.join(os.path.dirname(__file__), "db", "db.json"))
players_db = db_path.table('players')
# players_db.truncate()
tournaments_db = db_path.table('tournaments')


# tournaments_db.truncate()


# -----------------------------------------------------------------------------

class Tournament:
    def __init__(self, name, location, start_date, end_date, nb_round, r_time, description, players_ids,
                 tournament_ids, players_inst, rounds, matchs, finish):
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
        self.matchs = matchs
        self.finish = finish


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
        pass


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

    def update_all(self, obj, index):
        if obj.__class__.__name__ == "Players":
            players_db.update({k: getattr(obj, k) for (k, v) in self.const.player.items()}, doc_ids=index)
            return True
        elif obj.__class__.__name__ == "Tournament":
            for k, v in obj.__dict__.items():
                if isinstance(getattr(obj, k), dict):
                    tournaments_db.update({k: list(getattr(obj, k))})
                else:
                    tournaments_db.update({k: getattr(obj, k)})
            return True

    def update_player(self, varname, value, index):
        var = [{varname[i]: value[i]} for i in range(len(varname))]
        players_db.update({k: v for (k, v) in var}, doc_ids=index)

    def load(self, db, index):
        if db == "tournament":
            if isinstance(index, int):
                #print("db", tournaments_db.get(doc_id=index))
                return tournaments_db.get(doc_id=index)
            else:
                #print("db", tournaments_db.all())
                return tournaments_db.all()
        elif db == "players":
            if isinstance(index, int):
                #print("db", players_db.get(doc_id=index))
                return players_db.get(doc_id=index)
            else:
                #print("db", players_db.all())
                return players_db.all()
        return False

    def un_serialize_tournament(self, tournaments):
        return [values for keys, values in tournaments.items()]

    def un_serialize_player(self, players):
        #print("serialize", players)
        return [values for keys, values in players.items()]

