from task_2_2.modules.users import Users
from task_2_2.modules.quiz import Quiz
from task_2_2.database import db


class DatabaseQuerries():

    # Users querries
    def get_all_games(self, user):
        return user.quizzes.all()

    def count_admins(self):
        return Users.query.filter(Users.is_active == True, Users.is_admin == True).count()

    def new_admin(self, randuser):
        return Users(name=randuser.user, email='example@example.pl', password=randuser.hash_password(),
              is_active=True, is_admin=True)

    def new_user(self, user, hshd_pass):
        return Users(name=user['user_name'], email=user['user_email'], password=hshd_pass, is_active=True,
                             is_admin=False)

    def get_logged_user(self, login):
        return Users.query.filter(Users.name == login.user).first()

    def get_all_users(self):
        return Users.query.all()

    def get_user_if_logged(self, user_name, login):
        return Users.query.filter(Users.name == user_name, Users.name != login.user).first()

    def get_user_by_name(self, user_name):
        return Users.query.filter(Users.name == user_name).first()

    def check_name_if_occupied(self, name):
        return Users.query.filter(Users.name == name).count()

    def check_email_if_occupied(self, email):
        return Users.query.filter(Users.email == email).count()

    def change_user_status_active(self, user_name, login):
        user = self.get_user_if_logged(user_name=user_name, login=login)
        if user:
            user.is_active = (user.is_active + 1) % 2
            self.session_commit()
            return True

    def change_user_status_admin(self, user_name, login):
        user = self.get_user_if_logged(user_name=user_name, login=login)
        if user:
            user.is_admin = (user.is_admin + 1) % 2
            self.session_commit()
            return True

    # Quiz querries

    def get_result(self, topic, difficulty, user_points, user_id):
        return Quiz(topic=topic, difficulty=difficulty, correct_answers=user_points, user_id=user_id)


    # Session
    def session_add(self, db_object):
        db.session.add(db_object)

    def session_commit(self):
        db.session.commit()

    def session_delete(self, db_object):
        db.session.delete(db_object)