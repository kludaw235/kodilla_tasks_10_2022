from task_2_2 import app as app_test
from flask import Flask
# from pytest_mock import mocker, class_mocker
# from unittest.mock import Mock, MagicMock

def test_app_import_variables():
    from task_2_2 import app
    assert callable(app.app), '"app" is not callable'

def test_extensions_registered(mocker):
    ext_register = mocker.patch('task_2_2.database.db.init_app', return_value=True)
    app_test.register_extensions("test")
    ext_register.assert_called_once()

def test_app_creation(mocker):
    mocker.patch('task_2_2.app.register_extensions')
    app = app_test.create_app()
    assert isinstance(app, Flask)


# def test_app_creation(mocker):
#     # app = Mock()
#     x = mocker.patch('task_2_2.app.app.config.from_pyfile')
#     # app = Mock()
#     # app.config.from_pyfile = Mock()
#     # # mocker.patch.object(Flask, '__init__' , return_value=None)
#     # # mocker.patch.object(Flask)
#     # # x = mocker.patch('flask.Flask.app.config.from_pyfile')
#     # # app.config.from_pyfile = Mock()
#     app_test.create_app()
#     # app.config.from_pyfile.assert_called_once_with('config.cfg')
#     # assert app_test.create_app() == app
#     mocker.patch('task_2_2.app.register_extensions', return_value=1)
#     assert app_test.register_extensions('test') == 1
#     x().assert_called_once_with()
