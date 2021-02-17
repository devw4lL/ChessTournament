
class MainMenu:

    def __init__(self):
        self.terminal_width = 200
        self.terminal_height = 700

    def show_header(self, *args):
        [print(arg) for arg in args]

    def show_tournaments(self, tournaments, mode=''):
        """
        :param tournament: instance de la class Tournament.
        :return:
        """
        print(f'**  {mode}{"**":>{self.terminal_width - len(mode)-4}}\n')
        rows = [['**', f'{tournament.tournament_ids})', f'{tournament.name}', f'{tournament.location}',
                f'{tournament.start_date}', f'{tournament.end_date}'] for tournament in tournaments]
        rows.insert(0, ["**", "NUMERO", "NOM DU TOURNOI", "LIEU", "DATE DE DEBUT", "DATE DE FIN"])
        max_width = [max(map(len, col)) for col in zip(*rows)]
        [print("  ".join((val.ljust(width) for val, width in zip(row, max_width)))) for row in rows]
        print("\n\r\n\r")

    def show_players(self, players, mode=''):
        """
        :param player: Instance de la class Player.
        :param mode: Commentaire
        :return:
        """
        #print("show_players", player)
        print(f'**  {mode}{"**":>{self.terminal_width - len(mode)-4}}\n')
        rows = [['**', f'{player.player_ids})', f'{player.first_name}', f'{player.last_name}', f'{player.nickname}',
                f'{player.score}', f'{player.rank}'] for player in players]
        rows.insert(0, ["**", "NUMERO", "NOM JOUEUR", "PRENOM JOUEUR", "SURNOM", "SCORE", "RANK"])
        max_width = [max(map(len, col)) for col in zip(*rows)]
        [print("  ".join((val.ljust(width) for val, width in zip(row, max_width)))) for row in rows]
        print("\n\r\n\r")

    def show_rounds(self, mode, name):
        print(f'-----------> {mode} du {name}')

    def show_pairs(self, args, index):
        #print("show pairs", args, index)
        self.show_players(args, f'Nouvelle pair numéro {index}')

    def show_infos(self, infos):
        print(f'{infos}')


    def show_countdown(self, count_minutes, count_seconds):
        print(f'Temps restant {count_minutes} minutes et {count_seconds} secondes\n\r')

    def get_input(self, func, desc='', example=''):
        return input(f'{func} {desc} {example}\n\r')

