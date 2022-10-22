from task_2_2.routes import db_actions

db = db_actions.db

class Users(db_actions.db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.Text)
    is_active = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)

    quizzes = db.relationship('Quiz', backref='Users', lazy='dynamic')

    def __repr__(self):
        return f'User {self.id}/{self.name}'
