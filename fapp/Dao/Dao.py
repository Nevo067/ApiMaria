from fapp.model import Util
from fapp.model import db

UtilModel = Util()
class UserDao():
    @staticmethod
    def getAll():
        list = []
        for util in UtilModel.query.all():
            list.append(util.dumpJson())
        return list

    @staticmethod
    def postUser(user):
        print(user[UtilModel.FIELD_LOGIN])
        text = user[UtilModel.FIELD_LOGIN]
        new_util = Util()
        new_util.login = text
        db.session.add(new_util)
        db.session.commit()
        return new_util.dumpJson()





