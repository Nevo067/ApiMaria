from fapp import app
from flask_socketio import SocketIO

if __name__ == "__main__":
    socketio = SocketIO(app)
    socketio.run(app, debug=True)
