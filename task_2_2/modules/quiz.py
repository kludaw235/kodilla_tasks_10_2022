from .users import Users
from task_2_2.database import db

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20))
    difficulty = db.Column(db.String(20))
    correct_answers = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))

    def __repr__(self):
        return f'Quiz {self.id}/{self.topic}/{self.difficulty}/{self.correct_answers}'