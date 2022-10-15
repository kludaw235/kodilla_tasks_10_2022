from flask import Flask, redirect, url_for, render_template, session, flash, request, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import hashlib
import random
import binascii
import string
from task_2_2.scoreboard import Scoreboard

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
sb = Scoreboard()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.Text)
    is_active = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)

    quizzes = db.relationship('Quiz', backref='Users', lazy='dynamic')

    def __repr__(self):
        return f'User {self.id}/{self.name}'


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20))
    difficulty = db.Column(db.String(20))
    correct_answers = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))

    def __repr__(self):
        return f'Quiz {self.id}/{self.topic}/{self.difficulty}/{self.correct_answers}'


class UserPass:
    def __init__(self, user='', password=''):
        self.user = user
        self.password = password
        self.email = ''
        self.is_valid = False
        self.is_admin = False

    def hash_password(self):
        """Hash a password for storing."""
        # the value generated using os.urandom(60)
        os_random_static = b'\xf5\xba\xf6 \x041X\xdfG\xbc\xf8=\x11\x0b}\xe4\x8f\rG\xc2e\xca\x9c\x12\xed\xad\xd9\xad\xa6<S\xc39\x9a\xb4\x96n\x0e\xdd\x10\xae<F=qCK8\xeal\xc3\xe8\x9eY\xb4A5\xe9\x83\x85'
        salt = hashlib.sha3_256(os_random_static).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def get_random_user_password(self):
        random_user = ''.join(random.choice(string.ascii_lowercase) for i in range(3))
        self.user = random_user

        password_characters = string.ascii_letters  # + string.digits + string.punctuation
        random_password = ''.join(random.choice(password_characters) for i in range(3))
        self.password = random_password

    def login_user(self):
        user_record = Users.query.filter(Users.name == self.user).first()
        if user_record != None and self.verify_password(user_record.password, self.password):
            return user_record
        else:
            self.user = None
            self.password = None
            return None

    def get_user_info(self):
        user_info = Users.query.filter(Users.name == self.user).first()

        if user_info == None:
            self.is_valid = False
            self.is_admin = False
            self.email = ''
        elif user_info.is_active != 1:
            self.is_valid = False
            self.is_admin = False
            self.email = user_info.email
        else:
            self.is_valid = True
            self.is_admin = user_info.is_admin
            self.email = user_info.email


def verify_authorization(login_required=False, admin_required=False):
    login = UserPass(session.get('user'))
    login.get_user_info()
    if login_required and not login.is_valid:
        flash("Active account is required.")
        return
    if admin_required and not login.is_admin:
        flash("Admin account is required.")
        return
    return login


class Difficulty:
    def __init__(self, name="Medium", points_multiplier=2):
        self.name = name
        self.points_multiplier = points_multiplier

    def __repr__(self):
        return f"Difficulty {self.name} with {self.points_multiplier}x point multiplier"


class QuizSettings:
    def __init__(self):
        self.difficulties = []
        self.categories = []

    def load_difficulties(self):
        self.difficulties.append(Difficulty(name="Easy", points_multiplier=1))
        self.difficulties.append(Difficulty(name="Medium", points_multiplier=2))
        self.difficulties.append(Difficulty(name="Hard", points_multiplier=3))
        self.difficulties.append(Difficulty(name="Very hard", points_multiplier=4))

    def load_categories(self):
        self.categories.append("Movie")
        self.categories.append("Music")
        self.categories.append("Economy")
        self.categories.append("Animals")


@app.route('/init_app')
def init_app():
    db.create_all()
    # Check if there are users defined (at least one active admin required)
    active_admins = Users.query.filter(Users.is_active == True, Users.is_admin == True).count()

    if active_admins != None and active_admins > 0:
        flash('Application is already set-up. Nothing to do.')
        return redirect(url_for('index'))
    else:
        randuser = UserPass()
        randuser.get_random_user_password()
        new_admin = Users(name=randuser.user, email='example@example.pl', password=randuser.hash_password(),
                          is_active=True, is_admin=True)
        db.session.add(new_admin)
        db.session.commit()
        flash(f'User {randuser.user} with password | {randuser.password} | has been created.')
        return redirect(url_for('index'))


@app.route('/')
def index():
    login = verify_authorization()
    return render_template('index.html', active_menu='home', login=login)


@app.route('/new_quiz', methods=['GET', 'POST'])
def new_quiz():
    login = verify_authorization(login_required=True)
    if login == None:
        return redirect('login')

    settings = QuizSettings()
    settings.load_difficulties()
    settings.load_categories()

    if request.method == 'GET':
        return render_template('new_quiz.html', settings=settings, active_menu='new_quiz', login=login)
    else:
        difficulty = '' if 'difficulty' not in request.form else request.form['difficulty']
        category = '' if 'category' not in request.form else request.form['category']

        user = Users.query.filter(Users.name == login.user).first()
        user_points = random.randint(0, 10)
        quiz_result = Quiz(topic=category, difficulty=difficulty, correct_answers=user_points, user_id=user.id)
        db.session.add(quiz_result)
        db.session.commit()

        sb.update_score(user)
        return redirect(url_for('scoreboard'))


@app.route('/scoreboard')
def scoreboard():
    json_scoreboard = sb.get_scoreboard()
    return json_scoreboard


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = verify_authorization()

    if request.method == 'GET':
        return render_template('login.html', active_menu='login', login=login)
    else:
        user_name = '' if 'user_name' not in request.form else request.form['user_name']
        login_pass = '' if 'login_pass' not in request.form else request.form['login_pass']
        login = UserPass(user_name, login_pass)
        login_record = login.login_user()

        if login_record != None:
            session['user'] = user_name
            flash(f"Logon successful, welcome {user_name}")
            return redirect(url_for('index'))
        else:
            flash(f"Logon failed, try aqain...")
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        flash('You are logged out')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/users')
def users():
    login = verify_authorization(login_required=True, admin_required=True)
    if login == None:
        return redirect('login')
    users = Users.query.all()
    return render_template('users.html', active_menu='users', users=users, login=login)


@app.route('/user_status_change/<action>/<user_name>')
def user_status_change(action, user_name):
    login = verify_authorization(login_required=True, admin_required=True)
    if login == None:
        return redirect('login')

    if action == 'active':
        user = Users.query.filter(Users.name == user_name, Users.name != login.user).first()
        if user:
            user.is_active = (user.is_active + 1) % 2
            db.session.commit()
    elif action == 'admin':
        user = Users.query.filter(Users.name == user_name, Users.name != login.user).first()
        if user:
            user.is_admin = (user.is_admin + 1) % 2
            db.session.commit()

    return redirect(url_for('users'))


@app.route('/user_edit/<user_name>', methods=['GET', 'POST'])
def user_edit(user_name):
    login = verify_authorization(login_required=True, admin_required=True)
    if login == None:
        return redirect('login')

    user = Users.query.filter(Users.name == user_name).first()

    if user == None:
        flash('User doesn\'t exist')
        return redirect(url_for('users'))

    if request.method == 'GET':
        return render_template('edit_user.html', active_menu='users', user=user, login=login)
    else:
        new_email = user.email if 'user_email' not in request.form else request.form['user_email']
        new_pass = '' if 'user_pass' not in request.form else request.form['user_pass']

        try:
            if new_email != user.email:
                user = Users.query.filter(Users.name == user_name).first()
                user.email = new_email
                db.session.commit()
                flash('Email has been changed.')
        except exc.IntegrityError:
            flash('The e-mail address is already used!')
        else:
            if new_pass != '':
                user_pass = UserPass(user_name, new_pass)
                user = Users.query.filter(Users.name == user_name).first()
                user.password = user_pass.hash_password()
                db.session.commit()
                flash('Password has been changed.')

        return redirect(url_for('users'))


@app.route('/user_delete/<user_name>')
def user_delete(user_name):
    login = verify_authorization(login_required=True, admin_required=True)
    if login == None:
        return redirect('login')

    user = Users.query.filter(Users.name == user_name, Users.name != login.user).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    login = verify_authorization()

    message = None
    user = {}

    if request.method == 'GET':
        return render_template('new_user.html', active_menu='users', user=user, login=login)
    else:
        user['user_name'] = '' if 'user_name' not in request.form else request.form['user_name']
        user['user_email'] = '' if 'user_email' not in request.form else request.form['user_email']
        user['user_pass'] = '' if 'user_pass' not in request.form else request.form['user_pass']

        is_taken_name = Users.query.filter(Users.name == user['user_name']).count()
        is_taken_email = Users.query.filter(Users.email == user['user_email']).count()

        if user['user_name'] == '':
            message = f"Username cannot be empty"
        elif user['user_email'] == '':
            message = f"Email cannot be empty"
        elif user['user_pass'] == '':
            message = f"User's password cannot be empty"
        elif is_taken_name:
            message = f"Username {user['user_name']} is taken already"
        elif is_taken_email:
            message = f"E-mail {user['user_email']} is taken already"

        if not message:
            new_user = UserPass(user['user_name'], user['user_pass'])
            hshd_pass = new_user.hash_password()
            new_user = Users(name=user['user_name'], email=user['user_email'], password=hshd_pass, is_active=True,
                             is_admin=False)
            db.session.add(new_user)
            db.session.commit()
            flash(f"User {user['user_name']} created successfully")
            return redirect(url_for('login'))
        else:
            flash('Error message: ' + message)
            return render_template('new_user.html', active_menu='users', user=user, login=login)

# RANDOM USER
# User izo with password | gLz | has been created.
