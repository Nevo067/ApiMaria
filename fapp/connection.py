import mysql.connector as MS


class Connexion:

    def __init__(self):
        self.connexion = MS.connect(user='root', password='', host='127.0.0.1', buffered=True)
