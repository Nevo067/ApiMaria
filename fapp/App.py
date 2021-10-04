from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate



app = Flask(__name__)
CORS(app)
app.config.from_object('config')
socketio = SocketIO(app,cors_allowed_origins='*')
