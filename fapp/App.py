from flask import Flask
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.config
app.config.from_object('config')