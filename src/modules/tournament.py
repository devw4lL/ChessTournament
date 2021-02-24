
class Tournament:
    """
    La classe Tournaments représente entièrement un tournoi.
    Attention seul les ids (correspondant à la players_db) des joueurs sont stocké danq Tournament.
    """

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
        from src.models import Manager
        return Manager().save(self)  # Return db ids of new Tournament.

    def update_tournament(self):
        self.clear_players_inst()
        from src.models import Manager
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
        return True
