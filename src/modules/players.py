class Players:
    """
    Classe représentant un joueurs.
    """

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
        from src.models import Manager
        return Manager().save(self)  # Return db ids of new Player.

    def update_player(self):
        from src.models import Manager
        return Manager().update(self, self.player_ids)
