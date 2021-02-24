import re


class Validator:
    """
    La Classe Validator vérifie les saisie utilisateur suivant le type de saisie demandée.
    """

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

    def is_positiv_float(self, *args):
        try:
            [float(arg) for arg in list(args) if float(arg) >= 0]
            return True
        except TypeError as e:
            print(f'ERREUR: Validator.is_positiv_float {e}')
        except ValueError as e:
            print(f'ERREUR: Validator.is_positiv_float {e}')
