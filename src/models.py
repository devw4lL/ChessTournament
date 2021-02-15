import os

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
            print("update_players",obj, index)
            #players_db.update({k: getattr(obj, k) for (k, v) in self.const.player.items()}, doc_ids=index)
            return True
        elif obj.__class__.__name__ == "Tournament":
            print("update_tournament", obj, index)
            for k, v in obj.__dict__.items():
                if isinstance(getattr(obj, k), dict):
                    print("tourn if", {k: (getattr(obj, k))})
                    tournaments_db.update({k: list(getattr(obj, k))}, doc_ids=[index])
                else:
                    print("tourn_else", {k: getattr(obj, k)})
                    tournaments_db.update({k: getattr(obj, k)}, doc_ids=[index])
            return True

    def load(self, db, index):
        if db == "tournament":
            if isinstance(index, int):
                #print("db_load", tournaments_db.get(doc_id=index))
                return tournaments_db.get(doc_id=index)
            else:  # all
                #print("db_load", tournaments_db.all())
                return tournaments_db.all()
        elif db == "players":
            if isinstance(index, int):
                #print("db_load", players_db.get(doc_id=index))
                return players_db.get(doc_id=index)
            else:
                #print("db_load", players_db.all())
                return players_db.all()
        return False

    def un_serialize_tournament(self, tournaments):
        #print("serialize_tourn", tournaments, type(tournaments))
        return [values for keys, values in tournaments.items()]

    def un_serialize_player(self, players):
        """

        :param players: {'first_name': 'al', 'last_name': 'fred', 'b_date': '14/06/1988', 'sex': 'M',
                          'rank': '12', 'score': 0, 'player_ids': 1, 'opponents': [], 'nickname': 'Joueur_1'}
        :return: ['al', 'fred', '14/06/1988', 'M', '12', 0, 1, [], 'Joueur_1']
        """
        #print("serialize_players", players)
        return [values for keys, values in players.items()]




class serialize:
    def serialize_players_inst(self, obj):
            def __init__(self, **kwargs):
                for key, val in kwargs.items():
                    if type(val) == dict:
                        setattr(self, key, serialize(**val))
                    elif type(val) == list:
                        setattr(self, key, list(map(self.map_entry, val)))
                    else:  # this is the only addition
                        setattr(self, key, val)

    def map_entry(self, entry):
        if isinstance(entry, dict):
            return serialize(**entry)

        return entry

