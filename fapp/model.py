from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from fapp.App import app

db = SQLAlchemy(app)


class Util(db.Model):
    FIELD_ID = 'id'
    FIELD_LOGIN = 'login'
    FIELD_PASS = 'password'
    __tablename__ = 'Util'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    util = relationship("Message", back_populates="Util")

    Message = relationship("Message", back_populates="Util")

    def __init__(self, login):
        self.login = login

    def __init__(self):
        self.login = "test"

    def dumpJson(self):
        return {"id": self.id, "login": self.login,"password":self.password}


class Conversation(db.Model):
    __tablename__ = 'Conversation'

    FIELD_ID = "Id"
    FIELD_NOM = "nom"

    Id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=True)
    Message = relationship("Message", back_populates="Conversation")

    def dumpJson(self):
        return {"Id": self.id, "nom": self.nom}


class Message(db.Model):
    __tablename__ = 'Message'

    FIELD_ID = "IDMESSAGE"
    FIELD_TEXT = "TEXT"
    FIELD_IDCONVERSATION = "id_conversation";
    FIELD_UTIL = "Util"

    idMessage = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=True)

    id_conversation = db.Column(db.Integer, ForeignKey('Conversation.Id'))
    Conversation = relationship("Conversation", back_populates="Message")

    id_Util = db.Column(db.Integer, ForeignKey('Util.id'))
    Util = relationship("Util", back_populates="Message")

    def dumpJson(self):
        return {"IdMessage": self.idMessage, "text": self.text,
                "id_conversation": self.id_conversation,
                "id_Util": self.Util}

class Participant(db.Model):
    __tablename__ = 'Participant'

    FIELD_ID ="idParticipant"
    FIELD_IDUSER="idUser"
    FIELD_IDCONVERSATION="idconversation"
    FIELD_SURNOM="surnom"

    idParticipant = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, primary_key=True)
    idConversation =db.Column(db.Integer, primary_key=True)
    surnom = db.Column(db.String(200), nullable=True)

    def dumpJson(self):
        return {self.FIELD_ID: self.idParticipant, self.FIELD_IDUSER: self.idUser,
                self.FIELD_IDCONVERSATION: self.idConversation,
                self.FIELD_SURNOM: self.surnom}


db.create_all()
