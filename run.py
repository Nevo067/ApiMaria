from fapp import app
from fapp.App import socketio

from flask_socketio import SocketIO

if __name__ == "__main__":

    socketio.run(app, debug=True)
