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
    reponse =  flask.jsonify(Dao.UserDao.getAll())
    reponse.headers.add('Access-Control-Allow-Origin', '*')
    return reponse


@app.route("/User", methods=['POST'])
def post_User():
    DaoUser = UserDao();
    return flask.jsonify(Dao.UserDao.postUser((request.get_json()), DaoUser))


@app.route("/User/Update", methods=['POST'])
def update_User():
    return flask.jsonify(Dao.UserDao.updateUser(request.get_json()))


@app.route("/User/Delete", methods=['POST'])
def delete_User():
    return flask.jsonify(Dao.UserDao.deleteUser(request.get_json()))
