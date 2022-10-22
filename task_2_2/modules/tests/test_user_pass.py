from task_2_2.modules.user_pass import UserPass
import pytest
from pytest_mock import class_mocker

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

# Integrity tests

@pytest.fixture(params=['', 'SDF123!@#$%^&*()', 11, 11.1])
def passwords(request):
    return request.param

def test_hash_password(passwords):
    userpass_passwords = UserPass(passwords)
    stored_password = userpass_passwords.hash_password()
    assert userpass_passwords.verify_password(stored_password, userpass_passwords.password)

