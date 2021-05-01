from sqlalchemy import or_

from fapp.model import Util, Conversation, Message, Participant
from fapp.model import db

UtilModel = Util()
ConversationModel = Conversation()
MessageModel = Message
ParticipantModel = Participant()


class UserDao:
    @staticmethod
    def getAll():
        list = []
        for util in UtilModel.query.all():
            list.append(util.dumpJson())
        return list

    @staticmethod
    def getOneUserByName(userlogin):
        user = UtilModel.query.filter_by(login=userlogin).first()
        print(user, flush=True)
        if user is not None:
            return user.dumpJson()
        else:
            return False

    @staticmethod
    def getOneUserById(id):
        user = UtilModel.query.filter_by(id=id).first()
        print(user, flush=True)
        if user is not None:
            return user
        else:
            return False

    @staticmethod
    def IsExist(userJson):
        login = userJson[UtilModel.FIELD_LOGIN]
        password = userJson[UtilModel.FIELD_PASS]

        user = UtilModel.query.filter_by(login=login, password=password).first()
        if user is not None:
            return True
        else:
            return False

    @staticmethod
    def checkConnexionUser(userJson):
        login = userJson[UtilModel.FIELD_LOGIN]
        password = userJson[UtilModel.FIELD_PASS]

        user = UtilModel.query.filter_by(login=login, password=password).first()
        if user is not None:
            return user.dumpJson()
        else:
            return False

    @staticmethod
    def postUser(user, dao):
        print(user[UtilModel.FIELD_LOGIN], flush=True)
        login = user[UtilModel.FIELD_LOGIN]
        password = user[UtilModel.FIELD_PASS]
        new_util = Util()
        new_util.login = login
        new_util.password = password

        if not dao.isExistInUser(new_util):
            db.session.add(new_util)
            db.session.commit()
            return new_util.dumpJson()
        else:
            return "{}"

    @staticmethod
    def updateUser(user):
        id = user[UtilModel.FIELD_ID]
        login = user[UtilModel.FIELD_LOGIN]

        db.session.query(Util) \
            .filter_by(id=id) \
            .update({UtilModel.FIELD_LOGIN: login})

    @staticmethod
    def deleteUser(user):
        id = user[UtilModel.FIELD_ID]

        db.session.query(Util) \
            .filter_by(id=id) \
            .delete()

    # Method utilitaire
    @staticmethod
    def getAllUserPy():
        list = []
        for util in UtilModel.query.all():
            list.append(util)
        return list

    def isExistInUser(self, newUtil):
        for util in self.getAllUserPy():
            if newUtil.login == util.login:
                return True
            else:
                return False


# TODO:Test this class
class ConversationDao():
    @staticmethod
    def getAll():
        list = []
        for util in ConversationModel.query.all():
            list.append(util.dumpJson())
        return list

    @staticmethod
    def getConvById(id):
        conv = ConversationModel.query.filter_by(Id=id).first()
        return conv.dumpJson()

    @staticmethod
    def getConvByUserId(id):
        list = []
        for conv in ConversationModel.query.join(Participant) \
                .join(Util) \
                .filter(Util.id == id).all():
            list.append(conv.dumpJson())
        return list

    @staticmethod
    def getConvByUserAndAIdParticipant(idParticipant, id):
        list = []
        for conv in ConversationModel.query \
                .join(Participant) \
                .join(Util) \
                .filter_by(id=id, idParticipant=idParticipant).all():
            list.append(conv.dumpJson())
        return list

    @staticmethod
    def getConvByTwoParticipant(idParticipant1, idParticipant2):

        conv = ConversationModel.query \
            .join(Participant) \
            .filter((Participant.idParticipant == idParticipant1) & (Participant.idParticipant == idParticipant2)) \
            .first()
        return conv

    @staticmethod
    def postConversation(conv):
        nom = conv[ConversationModel.FIELD_NOM]
        convs = Conversation()
        convs.login = nom
        db.session.add(convs)
        db.session.commit()
        return convs

    @staticmethod
    def updateUser(user):
        id = user[ConversationModel.FIELD_ID]
        nom = user[ConversationModel.FIELD_NOM]

        db.session.query(Util) \
            .filter_by(id=id) \
            .update({ConversationModel: nom})

    @staticmethod
    def deleteUser(user):
        id = user[ConversationModel.FIELD_ID]

        db.session.query(ConversationModel) \
            .filter_by(id=id) \
            .delete()


class MessageDao():
    @staticmethod
    def getAll():
        list = []
        for util in MessageModel.query.all():
            list.append(util.dumpJson())
        return list

    @staticmethod
    def postMessage(conv):
        nom = conv[MessageModel.FIELD_TEXT]
        idConv = conv[MessageModel.FIELD_IDCONVERSATION]
        util = conv[MessageModel.FIELD_UTIL]

        convs = Message()
        convs.nom = nom
        convs.id_conversation = idConv
        convs.Util = util

        db.session.add(convs)
        db.session.commit()
        return convs.dumpJson()

    @staticmethod
    def updateUser(user):
        id = user[MessageModel.FIELD_ID]
        nom = user[MessageModel.FIELD_TEXT]
        idConv = user[MessageModel.FIELD_IDCONVERSATION]
        util = user[MessageModel.FIELD_UTIL]
        db.session.query(Util) \
            .filter_by(id=id) \
            .update({MessageModel: nom})

    @staticmethod
    def deleteUser(user):
        id = user[MessageModel.FIELD_ID]

        db.session.query(MessageModel) \
            .filter_by(id=id) \
            .delete()


class ParticipantDao:
    @staticmethod
    def getAll():
        list = []
        for part in Participant.query.all():
            list.append(part.dumpJson())
        return list

    @staticmethod
    def getParticipantByIdUser(id):
        Part = Participant.query.filter_by(idUser=id).first()
        return Part.dumpJson()

    @staticmethod
    def PostParticipant(id,idConv):
        part = Participant()
        part.idUser = id
        part.surnom = UserDao.getOneUserById(id).login
        part.idConversation = idConv

        db.session.add(part)
        db.session.commit()
        return part
