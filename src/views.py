
class MainMenu:

    def __init__(self):
        pass

    def show_header(self, *args):
        [print(arg) for arg in args]

    def show_tournaments(self, args):
        print(f'**  Entrer le numéro du tournoi à reprendre:       {"**":>149}\n')
        rows = [['**', f'{i+1})', f'{a[0]}', f'{a[1]}', f'{a[2]}', f'{a[3]}'] for i, a in enumerate(args)]
        rows.insert(0, ["**", "NUMERO", "NOM DU TOURNOI", "LIEU", "DATE DE DEBUT", "DATE DE FIN"])
        max_width = [max(map(len, col)) for col in zip(*rows)]
        [print("  ".join((val.ljust(width) for val, width in zip(row, max_width)))) for row in rows]

    def show_players(self, args):
        print(args)
        print(f'**  Entrer le numéro du joueur à éditer:           {"**":>149}\n')
        rows = [['**', f'{i+1})', f'{a[0]}', f'{a[1]}', f'{a[2]}', f'{a[3]}', f'{a[4]}'] for i, a in enumerate(args)]
        rows.insert(0, ["**", "NUMERO", "NOM JOUEUR", "PRENOM JOUEUR", "SURNOM", "SCORE", "RANK"])
        max_width = [max(map(len, col)) for col in zip(*rows)]
        [print("  ".join((val.ljust(width) for val, width in zip(row, max_width)))) for row in rows]

    def show_rounds(self, mode, name):
        print(f'{mode} du {name}')

    def edit_players(self, mode ):
        pass
    def show_countdown(self, count_minutes, count_seconds):
        print(f'Temps restant {count_minutes} minutes et {count_seconds} secondes')

    def get_input(self, func, desc='', example=''):
        return input(f'{func} {desc} {example}')
