from sqlalchemy import or_, desc, asc
import json
import requests
from fapp.model import Util, Conversation, Message, Participant
from fapp.model import db
from fapp.public_variable.Constant import save_file_url, idUserAi

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
            print("is not none")
            return user.dumpJson()
        else:
            return ""

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

    @staticmethod
    def get_user_by_id_participant(idPart):
        user = UtilModel.query.join(Participant).filter_by(IdParticipant=idPart).first()
        return user


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
        if len(list) < 0:
            return ""
        print(len(list))
        return list

    @staticmethod
    def get_conv_by_id_part(id):
        conv = ConversationModel.query \
            .join(Participant) \
            .filter(Participant.idUser == id) \
            .first()
        return conv

    @staticmethod
    def is_part_send_to_ai(idUser):
        conv = ConversationModel.query \
            .join(Participant) \
            .filter(Participant.idUser == idUser) \
            .first()
        listPart = ParticipantModel.query \
            .join(Conversation) \
            .filter(Conversation.Id == conv.Id).all()

        for part in listPart:
            if part.idUser == 4:
                return part
        return None

    @staticmethod
    def getConvByTwoUserId(id, id2):

        conv = ConversationModel.query.join(Participant) \
            .join(Util) \
            .filter(or_(Util.id == id, Util.id == id2)).first()

        return conv

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
    def getConvByMessage(message):
        return ConversationModel.query.join(Participant). \
            filter(Participant.idParticipant == message.idParticipant).first()

    @staticmethod
    def postConversation(conv):
        nom = conv[ConversationModel.FIELD_NOM]
        convs = Conversation()
        convs.login = nom
        db.session.add(convs)
        db.session.commit()
        return convs

    @staticmethod
    def updateConv(conv):
        id = conv.Id
        noms = conv.nom

        ConversationModel.query.filter_by(Id=id).update({"nom": noms})

    @staticmethod
    def updateConv(id, noms):

        ConversationModel.query.filter_by(Id=id).update({"nom": noms})
        db.session.commit()

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
    def getAllByConv(id):
        list = []
        for util in MessageModel.query. \
                join(Participant).filter(Participant.idConversation == id).all():
            list.append(util.dumpJson())
        return list

    @staticmethod
    def getAllMessageByConv(id):
        list = []
        for util in MessageModel.query.join(Participant).join(Conversation) \
                .filter(Conversation.Id == id).order_by(asc(MessageModel.messDate)).all():
            list.append(util.dumpJson())
        return list

    # à tester
    @staticmethod
    def postMessage(convn):
        conv = json.loads(convn)
        text = conv[MessageModel.FIELD_TEXT]
        idPart = conv[MessageModel.FIELD_IDPARTICIPANT]

        user = UserDao.get_user_by_id_participant(idPart)
        part = ConversationDao.is_part_send_to_ai(user.id)
        if part is not None:
            text_ai = AiDao.get_ai_text(text)
            messageAi = Message()
            messageAi.idParticipant = part.id
            messageAi.text = text_ai
            db.session.add(messageAi)

        convs = Message()
        convs.text = text
        convs.idParticipant = idPart

        db.session.add(convs)
        db.session.commit()
        print(convs.dumpJson())
        return convs

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
    def getParticipantByIdUserAndConv(idUser, IdConv):
        Part = Participant.query.join(Conversation) \
            .filter(Participant.idUser == idUser) \
            .filter(Conversation.Id == IdConv).first()
        return Part.dumpJson()

    # Check if two User is also in a conversation
    @staticmethod
    def CheckIfTwoParticipantIsAConv(id1, id2):
        part1List = Participant.query.filter_by(idUser=id1).all()
        part2List = Participant.query.filter_by(idUser=id2).all()

        for part1 in part1List:
            for part2 in part2List:
                if part1.idConversation == part2.idConversation:
                    return True

        return False

    @staticmethod
    def PostParticipant(id, idConv):
        part = Participant()
        part.idUser = id
        part.surnom = UserDao.getOneUserById(id).login
        part.idConversation = idConv

        db.session.add(part)
        db.session.commit()
        return part


class AiDao():
    @staticmethod
    def saveUrl(url):
        file_constant = open(save_file_url, "w")
        file_constant.write(url)
        return "ok"

    @staticmethod
    def get_ai_text(text):
        load = {'message': text}
        request = requests.post(save_file_url + "/message", load)
        val = request.json()
        return val
