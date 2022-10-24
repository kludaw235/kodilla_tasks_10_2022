from task_2_2.modules.users import Users

def test_user():
    user_id = 1
    name = "John"
    email = "fake@hotmail.com"
    user = Users(id=user_id, name=name, email=email)
    assert user.id == user_id
    assert user.name == name
    assert user.email == email
