from flask import Flask, render_template, jsonify, json
from fapp import App
from fapp.App import app
from flask import request

from fapp.Dao import Dao


@app.route("/", methods=['GET'])
def index():
    return render_template("test.html")


@app.route("/User", methods=['GET'])
def getAllUser():
    return jsonify(Dao.UserDao.getAll())


@app.route("/User", methods=['POST'])
def post_User():
    return jsonify(Dao.UserDao.postUser((request.get_json())))


@app.route("/User/Update", methods=['POST'])
def update_User():
    return jsonify(Dao.UserDao.updateUser(request.get_json()))


@app.route("/User/Delete", methods=['POST'])
def delete_User():
    return jsonify(Dao.UserDao.deleteUser(request.get_json()))
