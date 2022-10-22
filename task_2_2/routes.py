from .app import app
import random
from flask import redirect, url_for, render_template, session, flash, request, json
from sqlalchemy import exc
from .modules.quiz_settings import QuizSettings
# from .modules.users import Users
# from .modules.quiz import Quiz
from .modules.user_pass import UserPass, verify_authorization
from task_2_2.scoreboard import Scoreboard
from task_2_2.querries import DatabaseQuerries


sb = Scoreboard('myfile.json')
db_actions = DatabaseQuerries()


@app.route('/init_app')
def init_app():
    db_actions.db.create_all()
    # Check if there are users defined (at least one active admin required)
    # active_admins = Users.query.filter(Users.is_active == True, Users.is_admin == True).count()
    active_admins = db_actions.count_admins()

    if active_admins != None and active_admins > 0:
        flash('Application is already set-up. Nothing to do.')
        return redirect(url_for('index'))
    else:
        randuser = UserPass()
        randuser.get_random_user_password()
        # new_admin = Users(name=randuser.user, email='example@example.pl', password=randuser.hash_password(),
        #                   is_active=True, is_admin=True)
        new_admin = db_actions.new_admin(randuser=randuser)
        # db.session.add(new_admin)
        # db.session.commit()
        db_actions.session_add(new_admin)
        db_actions.session_commit()
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

    if request.method == 'GET':
        return render_template('new_quiz.html', settings=settings, active_menu='new_quiz', login=login)
    else:
        difficulty = '' if 'difficulty' not in request.form else request.form['difficulty']
        category = '' if 'category' not in request.form else request.form['category']

        # user = Users.query.filter(Users.name == login.user).first()
        user = db_actions.get_logged_user(login)
        user_points = random.randint(0, 10)
        # quiz_result = Quiz(topic=category, difficulty=difficulty, correct_answers=user_points, user_id=user.id)
        quiz_result = db_actions.get_result(category, difficulty, user_points, user.id)
        # db.session.add(quiz_result)
        # db.session.commit()
        db_actions.session_add(quiz_result)
        db_actions.session_commit()

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
    # users = Users.query.all()
    users = db_actions.get_all_users()
    return render_template('users.html', active_menu='users', users=users, login=login)


@app.route('/user_status_change/<action>/<user_name>')
def user_status_change(action, user_name):
    login = verify_authorization(login_required=True, admin_required=True)
    if login == None:
        return redirect('login')

    if action == 'active':
        # # user = Users.query.filter(Users.name == user_name, Users.name != login.user).first()
        # user = db_test.get_user_if_logged(user_name=user_name, login=login)
        # if user:
        #     user.is_active = (user.is_active + 1) % 2
        #     # db.session.commit()
        #     db_test.session_commit()
        db_actions.change_user_status_active(user_name, login)
        db_actions.db.session.commit()

    elif action == 'admin':
        # # user = Users.query.filter(Users.name == user_name, Users.name != login.user).first()
        # user = db_test.get_user_if_logged(user_name=user_name, login=login)
        # if user:
        #     user.is_admin = (user.is_admin + 1) % 2
        #     # db.session.commit()
        #     db_test.session_commit()
        db_actions.change_user_status_admin(user_name, login)
        db_actions.db.session.commit()

    return redirect(url_for('users'))


@app.route('/user_edit/<user_name>', methods=['GET', 'POST'])
def user_edit(user_name):
    login = verify_authorization(login_required=True, admin_required=True)
    if login == None:
        return redirect('login')

    # user = Users.query.filter(Users.name == user_name).first()
    user = db_actions.get_user_by_name(user_name=user_name)

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
                # user = Users.query.filter(Users.name == user_name).first()
                user = db_actions.get_user_by_name(user_name=user_name)
                user.email = new_email
                # db.session.commit()
                db_actions.session_commit()
                flash('Email has been changed.')
        except exc.IntegrityError:
            flash('The e-mail address is already used!')
        else:
            if new_pass != '':
                user_pass = UserPass(user_name, new_pass)
                # user = Users.query.filter(Users.name == user_name).first()
                user = db_actions.get_user_by_name(user_name=user_name)
                user.password = user_pass.hash_password()
                # db.session.commit()
                db_actions.session_commit()
                flash('Password has been changed.')

        return redirect(url_for('users'))


@app.route('/user_delete/<user_name>')
def user_delete(user_name):
    login = verify_authorization(login_required=True, admin_required=True)
    if login == None:
        return redirect('login')

    # user = Users.query.filter(Users.name == user_name, Users.name != login.user).first()
    user = db_actions.get_user_if_logged(user_name=user_name, login=login)
    # db.session.delete(user)
    db_actions.session_delete(user)
    db_actions.session_commit()
    # db.session.commit()
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

        # is_taken_name = Users.query.filter(Users.name == user['user_name']).count()
        # is_taken_email = Users.query.filter(Users.email == user['user_email']).count()
        is_taken_name = db_actions.check_name_if_occupied(user['user_name'])
        is_taken_email = db_actions.check_name_if_occupied(user['user_email'])

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
            # new_user = Users(name=user['user_name'], email=user['user_email'], password=hshd_pass, is_active=True,
            #                  is_admin=False)
            new_user = db_actions.new_user(user=user, hshd_pass=hshd_pass)
            # db.session.add(new_user)
            # db.session.commit()
            db_actions.session_add(new_user)
            db_actions.session_commit()
            flash(f"User {user['user_name']} created successfully")
            return redirect(url_for('login'))
        else:
            flash('Error message: ' + message)
            return render_template('new_user.html', active_menu='users', user=user, login=login)