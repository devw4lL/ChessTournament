from datetime import datetime, timedelta


class Tools:
    def __init__(self):
        pass

    def get_date(self):
        now = datetime.now()
        return now.strftime("%m/%d/%Y, %H:%M:%S")

    def sort_by_score(self, players):
        """
        :param players: List d'instances de l'object Players
        :return:
        [(16, <src.models.Players object at 0x00000265A57AE700>),......)]
        """
        print(sorted(players, key=lambda x: int(getattr(x, 'score'))))
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