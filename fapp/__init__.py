from flask import Flask
from .vieuw import app

from . import model

model.db.init_app(app)

@app.cli.command()
def init_db():
    model.init.db()


