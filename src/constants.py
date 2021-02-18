class Constants:

    def __init__(self):
        self.terminal_width = 200
        self.terminal_height = 700
        self.tournament_informations = [
            {"description": "Nom du tournoi\n", "varname": "name", "validator": ["is_alpha_sp"]},
            {"description": "Lieu du tournoi\n", "varname": "location", "validator": ["is_alpha_sp"]},
            {"description": "Date de début du tournoi\n", "varname": "start_date", "validator": ["is_date"]},
            {"description": "Date de fin du tournoi\n", "varname": "end_date", "validator": ["is_date"]},
            {"description": "Notre de rounds\n", "varname": "nb_round", "validator": ["is_positiv_int"]},
            {"description": "Durée d'un round\n", "varname": "r_time", "validator": ["is_positiv_int"]},
            {"description": "Description du tounoi\n", "varname": "description", "validator": ["is_printable"]}
        ]
        self.players_informations = [
            {"description": "Nom du joueur\n", "varname": "first_name", "validator": ["is_alpha_sp"]},
            {"description": "Prenom du joueur\n", "varname": "last_name", "validator": ["is_alpha_sp"]},
            {"description": "Date de naissance joueur\n", "varname": "b_date", "validator": ["is_date"]},
            {"description": "Sexe\n", "varname": "sex", "validator": ["is_sex"]},
            {"description": "Classement\n", "varname": "rank", "validator": ["is_positiv_int"]}
        ]
        self.tournament = {"name": "obj.name",
                           "location": "obj.location",
                           "start_date": "obj.start_date",
                           "end_date": "obj.end_date",
                           "nb_round": "obj.nb_round",
                           "r_time": "obj.r_time",
                           "description": "obj.description",
                           "players_ids": "obj.players_ids",
                           "tournament_ids": "obj.tournament_ids",
                           "players_inst": "obj.players_inst",
                           "rounds": "obj.rounds",
                           "finish": "obj.finish"
                           }
        self.player = {"first_name": "obj.first_name",
                       "last_name": "obj.last_name",
                       "b_date": "obj.b_date",
                       "sex": "obj.sex",
                       "rank": "obj.rank",
                       "score": "obj.score",
                       "player_ids": "obj.player_ids",
                       "opponents": "obj.opponents",
                       "nickname": "obj.nickname"
                       }
        self.players_nickname = ["Joueur_1", "Joueur_2", "Joueur_3", "Joueur_4",
                                 "Joueur_5", "Joueur_6", "Joueur_7", "Joueur_8"
                                 ]

        self.round_name = ["Round_1", "Round_2", "Round_3", "Round_4",
                           "Round_5", "Round_6", "Round_7", "Round_8"
                           ]

        self.header = (f'{"Bienvenu dans votre gestionnaire de tournoi":*^{self.terminal_width}}\n'
                       f'{"":*^{self.terminal_width}}\n'
                       f'**{"Entrer le numéro et valider avec la touche Entrer":^{self.terminal_width - 4}}**\n'
                       f'{"**":<0}{"**":>{self.terminal_width - 2}}\n'
                       f'{"":*^{self.terminal_width}}'
                       )

        self.main_menu = (f'**   1) Creér un nouveau tournoi.          {"**":>157}\n'
                          f'**   2) Reprendre un tournoi.              {"**":>157}\n'
                          f'**   3) Générer un rapport.                {"**":>157}\n'
                          f'**   4) Quitter.                           {"**":>157}'
                          )

        self.tournament_menu = (f'**    Entrer les informations concernant le nouveau tournoi: {"**":>139}\n'
                                f'**    Nom du tournoi, Lieu du tournoi, Date de debut (JJ/MM/AA), Date de fin, '
                                f'Nombre de rounds, Durée d\'un round, Description             {"**":>62}\n'
                                )

        self.new_player = (f'**    Entrer les informations concernant le nouveau joueur:                {"**":>125}\n'
                           f'**    Nom, Prenom, Date d\'anniversaire (JJ/MM/AA), sexe (M/F), Classement {"**":>126}\n'
                           )

        self.resume_menu = (f'**   1) Demarrer le nouveau tournoi.                       {"**":>141}\n'
                            f'**   2) Sauvgarder.                                        {"**":>141}\n'
                            f'**   3) Menu précédent.                                    {"**":>141}\n'
                            )

        self.round_menu = (f'**   1) Afficher le chronometre.                           {"**":>141}\n'
                           f'**   2) Lancer le round.                                   {"**":>141}\n'
                           f'**   3) Cloturer le round.                                 {"**":>141}\n'
                           f'**   4) Editer le score des joueurs.                       {"**":>141}\n'
                           f'**   5) Editer le classement des joueurs.                  {"**":>141}\n'
                           f'**   6) Sauvgarder.                                        {"**":>141}\n'
                           f'**   7) Menu précédent.                                    {"**":>141}\n'
                          )

        self.rank_menu = (
            f'**{"Entrer le numéro du joueurs, et son nouveau classement":^{self.terminal_width - 4}}**\n'
            f'**{"Séparer les informations avec une virgule":^{self.terminal_width - 4}}**\n'
            f'-----> EXEMPLE: 1, 85 \n'
            f'{"**":<0}{"**":>{self.terminal_width - 2}}\n'
            f'{"":*^{self.terminal_width}}'
                         )

        self.score_menu = (f'**   Entrer le numéro du joueurs, et son nouveau score:               {"**":>141}\n'
                           f'**   Séparer les informations avec une virgule:                       {"**":>141}\n'
                           f'-----> EXEMPLE: 1, 2 \n'
                           f'{"**":<0}{"**":>{self.terminal_width - 2}}\n'
                           f'{"":*^{self.terminal_width}}'
                           )

        self.end_tournament = (f'{"":*^{self.terminal_width}}\n'
                               f'**{"----------FIN DU TOURNOI----------":^{self.terminal_width - 4}}**\n'
                               f'{"":*^{self.terminal_width}}\n'
                               )

        self.quit_tournament = (f'**{"----------ATTENTION TOURNOI EN COURS----------":^{self.terminal_width - 4}}**\n'
                                f'**{"--VOULLEZ VOUS SAUVGARDER AVANT DE QUITTER ?--":^{self.terminal_width - 4}}**\n' 
                                f'**   1) OUI.                                               {"**":>141}\n'
                                f'**   2) NON.                                               {"**":>141}\n'
                               )

        self.report_menu = (f'**   1) Tout les joueurs par ordre alphabétique.             {"**":>139}\n'
                            f'**   2) Tout les joueurs par classement.                     {"**":>139}\n'
                            f'**   3) Tout les tournois.                                   {"**":>139}\n'
                            f'**   4) Tout les joeurs d\'un tournoi par odre alphabétique. {"**":>140}\n'
                            f'**   5) Tout les joeurs d\'un tournoi par classement.        {"**":>140}\n'
                            f'**   6) Tout les rounds d\'un tournoi.                       {"**":>140}\n'
                            f'**   7) Tout les matchs d\'un tournoi.                       {"**":>140}\n'
                            f'**   8) Menu précédent.                                      {"**":>140}\n'
                            )
