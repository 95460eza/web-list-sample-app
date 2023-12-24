
from flask import Flask

from .views import flask_web_app



# Connect sqlalchemy to your API
#models.db.init_app(flask_web_app)


# To use flask in Command Line Interface (CLI) mode
#@flask_web_app.cli.command()
#def init_db():
#    models.init_db()