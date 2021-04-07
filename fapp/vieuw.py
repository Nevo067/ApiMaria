import flask
from flask import Flask, render_template, jsonify, json
from fapp import App
from fapp.App import app
from flask import request

from fapp.Dao import Dao
from fapp.Dao.Dao import UserDao


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


@app.route('/User/IsExist/<login>/<password>', methods=['GET'])
def IsExistUser(login, password):
    reponse = flask.jsonify(Dao.UserDao.isExistInUser(login, password))
    return reponse


@app.route('/User/Check/<login>/<password>', methods=['GET'])
def Check(login, password):
    reponse = flask.jsonify(Dao.UserDao.checkConnexionUser(login, password))
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
