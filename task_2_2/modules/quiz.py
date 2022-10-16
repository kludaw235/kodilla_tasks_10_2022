from ..app import db
from .users import Users

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20))
    difficulty = db.Column(db.String(20))
    correct_answers = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))

    def __repr__(self):
        return f'Quiz {self.id}/{self.topic}/{self.difficulty}/{self.correct_answers}'