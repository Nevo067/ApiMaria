import flask
from flask_socketio import SocketIO, send, emit
from flask import Flask, render_template, jsonify, json
from sqlalchemy import null

from fapp import App
from fapp.App import app, socketio
from flask import request

from fapp.Dao import Dao
from fapp.Dao.Dao import UserDao, ConversationModel, ParticipantDao, UtilModel


@app.route("/", methods=['GET'])
def index():
    return render_template("test.html")


@app.route("/User", methods=['GET'])
def getAllUser():
    reponse = flask.jsonify(Dao.UserDao.getAll())
    reponse.headers.add('Access-Control-Allow-Origin', '*')
    return reponse


@app.route('/User/<login>', methods=['GET'])
def getOnUserByLogin(login):
    reponse = flask.jsonify(Dao.UserDao.getOneUserByName(login))
    return reponse


@app.route('/User/IsExist', methods=['POST'])
def IsExistUser():
    reponse = flask.jsonify(Dao.UserDao.IsExist(request.get_json()))
    if reponse:
        user = Dao.UserDao.getOneUserByName(request.get_json()[UtilModel.FIELD_LOGIN])

    return user


@app.route('/User/Check', methods=['POST'])
def Check():
    reponse = flask.jsonify(Dao.UserDao.checkConnexionUser(request.get_json()))
    return reponse


@app.route("/User", methods=['POST'])
def post_User():
    DaoUser = UserDao()
    print(request.get_json(), flush=True)
    reponse = flask.jsonify(Dao.UserDao.postUser((request.get_json()), DaoUser))
    reponse.headers.add('Access-Control-Allow-Origin', '*')
    return reponse


@app.route("/User/Update", methods=['POST'])
def update_User():
    return flask.jsonify(Dao.UserDao.updateUser(request.get_json()))


@app.route("/User/Delete", methods=['POST'])
def delete_User():
    return flask.jsonify(Dao.UserDao.deleteUser(request.get_json()))


@app.route("/Conv/findUser", methods=['POST'])
def conv_find_by_User():
    jobject = request.get_json()
    return flask.jsonify(Dao.ConversationDao.getConvByUserId(jobject[ConversationModel.FIELD_ID]))


# Enable to create a conv between two User
# id1 id2
@app.route("/Conv/CreateConv", methods=['POST'])
def conv_Create_Conv():
    jobject = request.get_json()
    id1 = jobject["id1"]
    id2 = jobject["id2"]

    if not Dao.ParticipantDao.CheckIfTwoParticipantIsAConv(id1, id2):
        #find user
        user1 = Dao.UserDao.getOneUserById(id1)
        user2 = Dao.UserDao.getOneUserById(id2)
        #post participant
        conv = Dao.ConversationDao.postConversation({"nom": "new Conv"})
        conv.nom = (user1.login + user2.login)
        #update conv
        Dao.ConversationDao.updateConv(conv)
        Dao.ParticipantDao.PostParticipant(id1, conv.Id)
        Dao.ParticipantDao.PostParticipant(id2, conv.Id)
    else:
        conv = Dao.ConversationDao.getConvByTwoUserId(id1, id2)
    return flask.jsonify(conv.dumpJson())


@app.route("/Message/Conv/<id>", methods=['GET'])
def getMessageConv(id):
    return flask.jsonify(Dao.MessageDao.getAllMessageByConv(id))

@app.route("/Message", methods=['POST'])
def postMessage():
    jobject = request.get_json()
    return  flask.jsonify(Dao.MessageDao.postMessage(jobject))


@app.route("/Participant/<conv>/<id>", methods=["GET"])
def getParticipantByIdUserAndIdConv(id, conv):
    return flask.jsonify(Dao.ParticipantDao.getParticipantByIdUserAndConv(id, conv))


@socketio.event
def connect():
    print('connexion')
    emit("coucou")


@socketio.event
def textx():
    print("xxx")
    send("coucou", broadcast=True)


@socketio.on('textx')
def testConnect(data):
    print("envoyé")
    socketio.emit("textx", data)
    print(data)

@socketio.on('/message')
def get_message(jsonmessage):
    convs = Dao.MessageDao.postMessage(jsonmessage)
    socketio.emit("/messageC", convs.dumpJson())
