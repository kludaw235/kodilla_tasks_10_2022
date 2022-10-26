import pytest
from webtest import TestApp
from task_2_2.app import app
from task_2_2.database import db
from task_2_2.modules.users import Users


@pytest.fixture(autouse=True)
def testapp():
    with app.app_context():
        db.create_all()
    return TestApp(app)

class TestRegistration:

    def test_can_register(self, testapp):
        with app.app_context():
            user_count = Users.query.count()
            response = testapp.get("/new_user")
            form = response.forms["new_user_form"]
            form["user_name"] = "endtest"
            form["user_email"] = "endtest@endtest"
            form["user_pass"] = "endtest"
            res = form.submit()
            assert res.status_code == 302
            assert Users.query.count() == user_count + 1

    @pytest.mark.parametrize('name, email', [
        ("difftest", "endtest@endtest"),
        ("endtest", "different_email")])
    def test_name_email_occupied(self, testapp, name, email):
        with app.app_context():
            user_count = Users.query.count()
            response = testapp.get("/new_user")
            form = response.forms["new_user_form"]
            form["user_name"] = name
            form["user_email"] = email
            form["user_pass"] = "endtest"
            res = form.submit()
            assert res.status_code == 200
            assert Users.query.count() == user_count

class TestLogin:

    def test_login(self, testapp):
        with app.app_context():
            response = testapp.get("/login")
            form = response.forms["login_form"]
            form["user_name"] = "admin"
            form["login_pass"] = "admin"
            res = form.submit()
            assert res.status_code == 302
            res.follow()
            assert res.headers['Location'] == '/'

    def test_login_failed(self, testapp):
        with app.app_context():
            response = testapp.get("/login")
            form = response.forms["login_form"]
            form["user_name"] = "xyz"
            form["login_pass"] = "password"
            res = form.submit()
            assert res.status_code == 302
            res.follow()
            assert res.headers['Location'] == '/login'

@pytest.fixture()
def admin_logged(testapp):
    with app.app_context():
        response = testapp.get("/login")
        form = response.forms["login_form"]
        form["user_name"] = "admin"
        form["login_pass"] = "admin"
        return form.submit().follow()

def test_user_delete(testapp, admin_logged):
    with app.app_context():
        user_count = Users.query.count()
        testapp.get("/user_delete/endtest")
        assert Users.query.count() == user_count - 1