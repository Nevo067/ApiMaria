from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO



app = Flask(__name__)
CORS(app)
app.config
app.config.from_object('config')
socketio = SocketIO(app,cors_allowed_origins='*')