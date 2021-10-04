from flask import Flask
from flask_migrate import Migrate

from .vieuw import app

from . import model

model.db.init_app(app)

migrate = Migrate(app, model.db)

@app.cli.command()
def init_db():
    model.init.db()


