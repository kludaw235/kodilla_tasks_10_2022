from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from task_2_2.scoreboard import Scoreboard

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
sb = Scoreboard()

import task_2_2.routes

# RANDOM USER
# User izo with password | gLz | has been created.
