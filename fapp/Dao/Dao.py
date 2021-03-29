from fapp.model import Util, Conversation, Message
from fapp.model import db

UtilModel = Util()
ConversationModel = Conversation()
MessageModel = Message


class UserDao():
    @staticmethod
    def getAll():
        list = []
        for util in UtilModel.query.all():
            list.append(util.dumpJson())
        return list

    @staticmethod
    def postUser(user, dao):
        print(user[UtilModel.FIELD_LOGIN])
        text = user[UtilModel.FIELD_LOGIN]
        new_util = Util()
        new_util.login = text

        if not dao.isExistInUser(user) :
            db.session.add(new_util)
            db.session.commit()
            return new_util.dumpJson()
        else :
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

    #Method utilitaire
    @staticmethod
    def getAllUserPy():
        list = []
        for util in UtilModel.query.all():
            list.append(util)
        return list

    def isExistInUser(self,newUtil):
        for util in self.getAllUserPy():
            if newUtil.login == util.login:
                return True
            else:
                return False



class ConversationDao():
    @staticmethod
    def getAll():
        list = []
        for util in ConversationModel.query.all():
            list.append(util.dumpJson())
        return list

    @staticmethod
    def postConversation(conv):
        nom = conv[ConversationModel.FIELD_NOM]
        convs = Conversation()
        convs.login = nom
        db.session.add(convs)
        db.session.commit()
        return convs.dumpJson()

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
