from task_2_2.modules.user_pass import UserPass
import pytest
from unittest.mock import Mock
from pytest_mock import mocker

def test_Scoreboard_import():
    from task_2_2.modules.user_pass import UserPass
    assert callable(UserPass), '"UserPass" is not callable'

@pytest.fixture()
def userpass():
    return UserPass()

def test_random_user_3_signs_string(userpass):
    userpass.get_random_user_password()
    assert len(userpass.user) == 3
    assert isinstance(userpass.user, str)

def test_random_password_3_signs_string(userpass):
    userpass.get_random_user_password()
    assert len(userpass.password) == 3
    assert isinstance(userpass.password, str)

@pytest.fixture()
def user_mock():
    user = Mock()
    user.password.return_value = 'password'
    return user

def test_login_user_valid(mocker, userpass, user_mock):
    mocker.patch('task_2_2.querries.DatabaseQuerries.get_user_by_name', return_value=user_mock)
    mocker.patch('task_2_2.modules.user_pass.UserPass.verify_password', return_value=True)
    assert userpass.login_user() == user_mock


@pytest.mark.parametrize('valid_user, valid_password', [
    (True, False),
    (None, True),
    (None, False)])
def test_login_user_invalid(mocker, userpass, user_mock, valid_user, valid_password):
    if valid_user:
        valid_user = user_mock
    mocker.patch('task_2_2.querries.DatabaseQuerries.get_user_by_name', return_value=valid_user)
    mocker.patch('task_2_2.modules.user_pass.UserPass.verify_password', return_value=valid_password)
    assert userpass.login_user() == None

def test_user_info_none(mocker, userpass):
    mocker.patch('task_2_2.querries.DatabaseQuerries.get_user_by_name', return_value=None)
    userpass.get_user_info()
    assert userpass.is_valid == False
    assert userpass.is_admin == False
    assert userpass.email == ''

def test_user_info_not_active(mocker, userpass):
    user = Mock()
    user.is_active = False
    user.email = 'test_not_active'
    mocker.patch('task_2_2.querries.DatabaseQuerries.get_user_by_name', return_value=user)
    userpass.get_user_info()
    assert userpass.is_valid == False
    assert userpass.is_admin == False
    assert userpass.email == 'test_not_active'

def test_user_info_active(mocker, userpass):
    user = Mock()
    user.email = 'test_active'
    user.is_active = True
    user.is_admin = True
    mocker.patch('task_2_2.querries.DatabaseQuerries.get_user_by_name', return_value=user)
    userpass.get_user_info()
    assert userpass.is_valid == True
    assert userpass.is_admin == True
    assert userpass.email == 'test_active'



# Integrity tests

@pytest.fixture(params=['', 'SDF123!@#$%^&*()', 11, 11.1])
def passwords(request):
    return request.param

def test_hash_password(passwords):
    userpass_passwords = UserPass(passwords)
    stored_password = userpass_passwords.hash_password()
    assert userpass_passwords.verify_password(stored_password, userpass_passwords.password)