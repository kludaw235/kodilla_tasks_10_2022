from task_2_2.modules.user_pass import UserPass
import pytest
from pytest_mock import class_mocker

def test_Scoreboard_import():
    from task_2_2.modules.user_pass import UserPass
    assert callable(UserPass), '"UserPass" is not callable'

@pytest.fixture()
def userpass():
    return UserPass()

# Integrity tests

@pytest.fixture(params=['', 'SDF123!@#$%^&*()', 11, 11.1])
def passwords(request):
    return request.param

def test_hash_password(passwords):
    userpass_passwords = UserPass(passwords)
    stored_password = userpass_passwords.hash_password()
    assert userpass_passwords.verify_password(stored_password, userpass_passwords.password)