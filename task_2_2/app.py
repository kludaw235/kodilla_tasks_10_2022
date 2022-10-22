from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config.from_pyfile('config.cfg')
# db = SQLAlchemy(app)

from task_2_2.database import db



def register_extensions(app):
    db.init_app(app)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.cfg')

    register_extensions(app)

    return app

app = create_app()




import task_2_2.routes




# RANDOM USER
# User izo with password | gLz | has been created.
