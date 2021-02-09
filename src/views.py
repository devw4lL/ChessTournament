
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
        print("\n\r\n\r")

    def show_players(self, args, mode=''):
        """

        :param args: [['al', 'fred', '14/06/1988', 'M', '12', 0, 1, [], 'Joueur_1'], ....]
        :param mode: Commentaire
        :return:
        """
        #print("show_players", args)
        print(f'**  {mode}           {"**":>149}\n')
        rows = [['**', f'{a[6]})', f'{a[0]}', f'{a[1]}', f'{a[8]}', f'{a[5]}', f'{a[4]}'] for a in args]
        rows.insert(0, ["**", "NUMERO", "NOM JOUEUR", "PRENOM JOUEUR", "SURNOM", "SCORE", "RANK"])
        max_width = [max(map(len, col)) for col in zip(*rows)]
        [print("  ".join((val.ljust(width) for val, width in zip(row, max_width)))) for row in rows]
        print("\n\r\n\r")

    def show_rounds(self, mode, name):
        print(f'-----------> {mode} du {name}')

    def show_pairs(self, args, index):
        #print("show pairs", args, index)
        self.show_players(args, f'Nouvelle pair numéro {index}')

    def edit_player(self, player, index, status=''):
        self.show_players([player], f'EDITION DU JOUEUR: {index} {status}         ')

    def get_new_score(self):
        return self.get_input("Entrer le nouveau", "score", "EXEMPLE: 1")

    def get_new_rank(self):
        return self.get_input("Entrer le nouveau", "classement", "EXEMPLE: 25")


    def show_countdown(self, count_minutes, count_seconds):
        print(f'Temps restant {count_minutes} minutes et {count_seconds} secondes\n\r')

    def get_input(self, func, desc='', example=''):
        return input(f'{func} {desc} {example}\n\r')
