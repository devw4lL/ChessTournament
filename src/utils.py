from datetime import datetime, timedelta


class Tools:
    def __init__(self):
        pass

    def get_date(self):
        now = datetime.now()
        return now.strftime("%m/%d/%Y, %H:%M:%S")

    def sort_by_score(self, players):
        """
        :param players: List, Liste d'instances d'object Players.
        :return List, Liste d'instances d'object Players triés par score.
        """
        return sorted(players, key=lambda x: int(getattr(x, 'score')))

    def sort_by_rank(self, players):
        """
        :param players: List, Liste d'instances d'object Players.
        :return List, Liste d'instances d'object Players triés par classement.
        """
        return sorted(players, key=lambda x: int(getattr(x, 'rank')), reverse=True)

    def sort_by_alpha(self, players):
        """
        :param players: List, Liste d'instances d'object Players.
        :return List, Liste d'instances d'object Players triés par ordre alphabétique du nom.
        """
        return sorted(players, key=lambda x: getattr(x, 'first_name'), reverse=True)

    def compare_score_and_rank(self, player_one, player_two):
        """
        Compare les joeurs par score, si les joeur ont les même score on trie par classement.
        :param player_one: Premier joueur de la pair.
        :param player_two: Deuxième joueur de la pair.
        :return: list d'une paire de joueurs triés.
        """
        if player_one.score == player_two.score:
            if player_one.rank >= player_two.rank:
                return [player_one, player_two]
        return [player_two, player_one]

    def compare_by_opponents(self, potential_pairs, p_by_score):
        """
        Vérifie que les joueurs d'une pair générée par compare_by_score_and_rank n'ont pas déjà joués enssemble.
        Si les joueurs ce sont déjà affronté ont associe le joueur suivant.
        :param potential_pairs: Pair de joueur généré précédement.
        :param p_by_score: Liste des joueurs triés par score.
        :return: list d'une paire de joueurs triés.
        """
        if potential_pairs[0][0].player_ids in potential_pairs[0][1].opponents:
            for i in range(1, len(p_by_score)-1):
                if not potential_pairs[0][0].player_ids in p_by_score[i+1].opponents:
                    return [potential_pairs[0][0], p_by_score[i+1]]
        return [potential_pairs[0][0], potential_pairs[0][1]]