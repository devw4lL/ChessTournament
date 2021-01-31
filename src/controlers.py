import re
import time
from datetime import datetime, timedelta

from src.constants import Constants
from src.views import MainMenu
from src.models import Tournament, Players, Manager


class Controler:

    def __init__(self):
        self.menu = MainMenu()
        self.const = Constants()
        self.db = Manager()
        self.tools = Tools()
        self.players_list = []

    def get_infos(self, mode):
        for item in getattr(self.const, mode):
            item['varname'] = self.menu.get_input(item['description'])
            for validator in item['validator']:
                while not getattr(Validator(), validator)(item['varname']):
                    item['varname'] = self.menu.get_input(item['description'])
        return True

    def tournament_start_up(self):
        self.menu.show_header(self.const.tournament_menu)
        if self.add_tournament():
            self.menu.show_header(self.const.new_player)
            if self.add_player():
                return True

    def get_tournaments(self, index, finish):
        return [self.db.un_serialize_tournament(args) for args in
                self.db.load("tournament", index) if args['finish'] == finish]

    def get_players(self, index):
        if index == "all":
            return [args for args in [self.db.un_serialize_player(self.db.load("players", "all"))]]
        else:
            return [args for args in [self.db.un_serialize_player(self.db.load("players", index)) for index in
                                      self.tourn.players_ids]]

    def get_countdown(self, r_time, status):
        stop = datetime.now() + timedelta(minutes=int(r_time))
        while status:
            difference = stop - datetime.now()
            days, seconds = difference.days, difference.seconds
            count_hours = days * 24 + seconds // 600
            count_minutes = (seconds % 3600) // 60
            count_seconds = seconds % 60
            if difference.days == 0 and count_hours == 0 and count_minutes == 0 and count_seconds == 0:
                return False
            self.menu.show_countdown(count_minutes, count_seconds)
            time.sleep(1)

    def start_tournament(self, index):
        self.tourn = Tournament(*self.db.un_serialize_tournament(dict(self.db.load('tournament', index))))
        [self.tourn.players_inst.update({a[0]: a[1]}) for a in
         [(*[varname[5]], Players(*varname)) for varname in
          [self.db.un_serialize_player(self.db.load("players", index)) for index in self.tourn.players_ids]]]
        self.get_first_pairs()

    def add_tournament(self):
        if self.get_infos('tournament_informations'):
            tourn_infos = [item['varname'] for item in self.const.tournament_informations]
            self.tourn = Tournament(name=tourn_infos[0], location=tourn_infos[1], start_date=tourn_infos[2],
                                    end_date=tourn_infos[3], nb_round=tourn_infos[4], r_time=tourn_infos[5],
                                    description=tourn_infos[6], players_ids=[], players_inst={}, rounds=[],
                                    matchs=[], finish=False)
        return True

    def add_player(self):
        for i in range(8):
            self.get_infos('players_informations')
            player = [item['varname'] for item in self.const.players_informations]
            player_infos = Players(first_name=player[0], last_name=player[1], b_date=player[2],
                                   sex=player[3], rank=player[4], index=i + 1, score=0, opponents=[],
                                   nickname=self.const.players_nickname[i])
            self.tourn.players_ids.append(self.db.save(player_infos))
        self.db.save(self.tourn)
        return True

    def get_first_pairs(self):
        players_by_rank = self.tools.sort_by_rank(self.tourn.players_inst)
        print(players_by_rank)
        players_inst_list = [k[1] for k in players_by_rank]
        pairs = [[players_inst_list[i], players_inst_list[i + len(players_inst_list) // 2]] for i in
                 range(len(players_inst_list) // 2)]
        self.update_opponents(pairs)
        return pairs

    def update_opponents(self, pairs_list):
        for player in pairs_list:
            self.tourn.players_inst[getattr(player[0], 'index')].opponents.append(getattr(player[1], 'index'))
            self.tourn.players_inst[getattr(player[1], 'index')].opponents.append(getattr(player[0], 'index'))

    def end_round(self):
        pass

    def edit_player_score(self, index):
        pass

    def edit_player_rank(self):
        pass

    def save_all(self):
        pass


class Tools:
    def __init__(self):
        pass



    def get_pairs(self, players):
        for players in players:
            print(players['nickname'])

    def get_date(self):
        now = datetime.now()
        return now.strftime("%m/%d/%Y, %H:%M:%S")

    def sort_by_score(self, players):
        return sorted(players.items(), key=lambda x: getattr(x[1], 'score'), reverse=True)

    def sort_by_rank(self, players):
        return sorted(players.items(), key=lambda x: getattr(x[1], 'rank'), reverse=True)

    def sort_by_alpha(self, players):
        return sorted(players.items(), key=lambda x: getattr(x[1], 'first_name'), reverse=True)


class Validator:

    def is_alpha_sp(self, *args):
        p = re.compile(r'[a-zA-Z\s-]+')
        try:
            return all([True if len(re.search(p, arg)[0]) == len(arg) else False for arg in args])
        except TypeError as e:
            print(f'ERREUR: Valisator.is_alpha {e}')

    def is_printable(self, *args):
        p = re.compile(r'^[a-zA-Z.,;:\s-]+')
        try:
            return all([True if len(re.search(p, arg)[0]) == len(arg) else False for arg in args])
        except TypeError as e:
            print(f'ERREUR: Valisator.is_printable {e}')

    def is_date(self, *args):
        date_p = re.compile(r'^((\d\d\/){2}\d\d)')
        try:
            return all([True if re.match(date_p, arg) is not None else False for arg in args])
        except TypeError as e:
            print(f'ERREUR: Validator.is_date {e}')

    def is_sex(self, arg):
        return True if arg in ["M", "F"] else False

    def is_positiv_int(self, *args):
        try:
            [int(arg) for arg in list(args) if int(arg) >= 0]
            return True
        except TypeError as e:
            print(f'ERREUR: Validator.is_positiv_int {e}')
        except ValueError as e:
            print(f'ERREUR: Validator.is_positiv_int {e}')
