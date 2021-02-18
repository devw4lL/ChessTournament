class MainMenu:

    def __init__(self):
        self.terminal_width = 200
        self.terminal_height = 700

    def show_header(self, *args):
        [print(arg) for arg in args]

    def show_tournaments(self, tournaments, mode=''):
        """
        :param tournament: instance de la class Tournament.
        """
        print(f'**  {mode}{"**":>{self.terminal_width - len(mode) - 4}}\n')
        rows = [['**', f'{tournament.tournament_ids})', f'{tournament.name}', f'{tournament.location}',
                 f'{tournament.start_date}', f'{tournament.end_date}'] for tournament in tournaments]
        rows.insert(0, ["**", "NUMERO", "NOM DU TOURNOI", "LIEU", "DATE DE DEBUT", "DATE DE FIN"])
        max_width = [max(map(len, col)) for col in zip(*rows)]
        [print("  ".join((val.ljust(width) for val, width in zip(row, max_width)))) for row in rows]
        print("\n\r\n\r")
        return True

    def show_players(self, players, mode=''):
        """
        :param player: Instance de la class Player.
        :param mode: Commentaire
        """
        # print("show_players", player)
        print(f'**  {mode}{"**":>{self.terminal_width - len(mode) - 4}}\n')
        rows = [['**', f'{player.player_ids})', f'{player.first_name}', f'{player.last_name}', f'{player.nickname}',
                 f'{player.score}', f'{player.rank}'] for player in players]
        rows.insert(0, ["**", "NUMERO", "NOM JOUEUR", "PRENOM JOUEUR", "SURNOM", "SCORE", "RANK"])
        max_width = [max(map(len, col)) for col in zip(*rows)]
        [print("  ".join((val.ljust(width) for val, width in zip(row, max_width)))) for row in rows]
        print("\n\r\n\r")
        return True

    def show_rounds_status(self, mode, name):
        print(f'-----------> {mode} du {name}')
        return True

    def show_rounds(self, rounds):
        """
        :param rounds: List, Liste de rounds généré par controler.parse_rounds
        """
        rows = [['**', f'{r[0]}', f'{r[1]}', f'{r[2]}'] for r in rounds]
        rows.insert(0, ["**", "ROUND", "DATE ET HEURE DE DEBUT", "DATE ET HEURE DE FIN"])
        max_width = [max(map(len, col)) for col in zip(*rows)]
        [print("  ".join((val.ljust(width) for val, width in zip(row, max_width)))) for row in rows]
        print("\n\r\n\r")
        return True

    def show_matchs(self, matchs):
        """
        :param matchs: List, Liste de matchs généré par controler.parse_rounds
        """
        rows = [['**', f'{match[5]}', f'{match[1]}', f'{match[0]}', f'{match[3]}',
                 f'{match[4]}'] for match in matchs]
        rows.insert(0, ["**", "ROUND", "GAGNANT", "SCORE", "PERDANT", "SCORE"])
        max_width = [max(map(len, col)) for col in zip(*rows)]
        [print("  ".join((val.ljust(width) for val, width in zip(row, max_width)))) for row in rows]
        print("\n\r\n\r")
        return True

    def show_pairs(self, args, index):
        self.show_players(args, f'Nouvelle pair numéro {index}')
        return True

    def show_infos(self, infos):
        print(f'{infos}')
        return True

    def show_countdown(self, count_minutes, count_seconds):
        print(f'Temps restant {count_minutes} minutes et {count_seconds} secondes\n\r')
        return True

    def get_input(self, func, desc='', example=''):
        return input(f'{func} {desc} {example}\n\r')
