from flask_sqlalchemy import SQLAlchemy

from fapp.App import app

db = SQLAlchemy(app)


class Util(db.Model):
    FIELD_ID = 'id'
    FIELD_LOGIN = 'login'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(200), nullable=False)

    def __init__(self, login):

        self.login = login

    def __init__(self):
        self.login = "test"


    def dumpJson(self):
        return {"id": self.id, "login": self.login}

class Conversation(db.Model):
    idConversation =db.Column(db.Integer, primary_key=True)



db.create_all()
