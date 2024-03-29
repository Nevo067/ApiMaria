from datetime import datetime

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

    Participant = relationship("Participant", back_populates="Util")

    def __init__(self, login):
        self.login = login

    def __init__(self):
        self.login = "test"

    def dumpJson(self):
        return {"id": self.id, "login": self.login}


class Conversation(db.Model):
    __tablename__ = 'Conversation'

    FIELD_ID = "Id"
    FIELD_NOM = "nom"

    Id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=True)

    Participant = relationship("Participant", back_populates="Conversation")

    def dumpJson(self):
        return {"Id": self.Id, "nom": self.nom}


class Message(db.Model):
    __tablename__ = 'Message'

    FIELD_ID = "IDMESSAGE"
    FIELD_TEXT = "TEXT"
    FIELD_IDPARTICIPANT = "idParticipant"
    FIELD_MESSDATE = "MESSDATE"

    idMessage = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=True)
    messDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    idParticipant = db.Column(db.Integer, ForeignKey("Participant.idParticipant"))
    Participant = relationship("Participant", back_populates="Message")

    def dumpJson(self):
        return {"IdMessage": self.idMessage, "text": self.text,
                "idParticipant": self.idParticipant}


class Participant(db.Model):
    __tablename__ = 'Participant'

    FIELD_ID = "idParticipant"
    FIELD_IDUSER = "idUser"
    FIELD_IDCONVERSATION = "idconversation"
    FIELD_SURNOM = "surnom"

    idParticipant = db.Column(db.Integer, primary_key=True)

    idUser = db.Column(db.Integer, ForeignKey('Util.id'))
    Util = relationship("Util", back_populates="Participant")

    idConversation = db.Column(db.Integer, ForeignKey('Conversation.Id'))
    Conversation = relationship("Conversation", back_populates="Participant")

    Message = relationship("Message", back_populates="Participant")

    surnom = db.Column(db.String(200), nullable=True)

    def dumpJson(self):
        return {self.FIELD_ID: self.idParticipant, self.FIELD_IDUSER: self.idUser,
                self.FIELD_IDCONVERSATION: self.idConversation,
                self.FIELD_SURNOM: self.surnom}


db.create_all()
