from task_2_2.database import db
from task_2_2.app import app
from task_2_2.querries import DatabaseQuerries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from sqlalchemy.orm.exc import UnmappedInstanceError
from webdriver_manager.firefox import GeckoDriverManager
import pytest

URL = 'http://127.0.0.1:5000/'
SERVICE = Service(GeckoDriverManager().install())


@pytest.fixture(name='clear')
def clear_user_before_tests():
    with app.app_context():
        db.create_all()
        dq = DatabaseQuerries()
        try:
            test_user = dq.get_user_by_name('TestUser')
            dq.session_delete(test_user)
            dq.session_commit()
        except UnmappedInstanceError:
            pass


@pytest.fixture()
def browser():
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    options.add_argument('--headless')
    driver = webdriver.Firefox(service=SERVICE, options=options)
    driver.implicitly_wait(2)
    driver.get(URL)
    yield driver
    driver.close()


@pytest.fixture()
def browser_new_user(browser):
    # Go to add new user form
    browser.find_element(by=By.XPATH, value='//*[@id="navbarDropdown"]').click()
    browser.find_element(by=By.XPATH, value='/html/body/nav/div/div/ul/li[2]/div/a').click()
    # Get attributes
    login = browser.find_element(by=By.XPATH, value='//*[@id="user_name"]')
    email = browser.find_element(by=By.XPATH, value='//*[@id="user_email"]')
    password = browser.find_element(by=By.XPATH, value='//*[@id="user_pass"]')
    return browser, login, email, password

@pytest.fixture()
def browser_login(browser):
    # Go to login form
    browser.find_element(by=By.XPATH, value='/html/body/nav/div/div/ul/li[3]/a').click()
    login = browser.find_element(by=By.XPATH, value='//*[@id="user_name"]')
    password = browser.find_element(by=By.XPATH, value='//*[@id="login_pass"]')
    return browser, login, password

def test_create_new_user(browser_new_user, clear):
    browser = browser_new_user[0]
    # Fill up the form
    browser_new_user[1].send_keys("TestUser")
    browser_new_user[2].send_keys("test@email.com")
    browser_new_user[3].send_keys("password")
    # Create new user
    browser.find_element(by=By.XPATH, value='/html/body/div/form/div[4]/div[2]/input').click()
    create_user_message = browser.find_element(by=By.XPATH, value='/html/body/div[1]/div/strong')
    assert create_user_message.text == "User TestUser created successfully"


@pytest.mark.parametrize('login, email, password, message', [
    ('', 'Test@email.com', 'password', 'Username cannot be empty'),
    ('TestUser', '', 'password', 'Email cannot be empty'),
    ('TestUser', 'test@email.com', '', 'User\'s password cannot be empty'),
    ('TestUser', 'diff@email.com', 'password', 'Username TestUser is taken already'),
    ('DiffUser', 'test@email.com', 'password', 'E-mail test@email.com is taken already')])
def test_create_new_user_failure(browser_new_user, login, email, password, message):
    browser = browser_new_user[0]
    # Fill up the form
    browser_new_user[1].send_keys(login)
    browser_new_user[2].send_keys(email)
    browser_new_user[3].send_keys(password)
    # Create new user
    browser.find_element(by=By.XPATH, value='/html/body/div/form/div[4]/div[2]/input').click()
    create_user_message = browser.find_element(by=By.XPATH, value='/html/body/div[1]/div/strong')
    assert create_user_message.text == f"Error message: {message}"





def test_login_logout(browser_login):
    browser = browser_login[0]
    # Fill up the login form
    browser_login[1].send_keys("TestUser")
    browser_login[2].send_keys("password")
    # Login confirm
    browser.find_element(by=By.XPATH, value='/html/body/div/form/div[3]/div[2]/input').click()
    login_message = browser.find_element(by=By.XPATH, value='/html/body/div[1]/div/strong')
    assert login_message.text == "Logon successful, welcome TestUser"
    assert browser.current_url == URL
    # Logout
    browser.find_element(by=By.XPATH, value='/html/body/nav/div/div/ul/li[5]/a').click()
    logout_message = browser.find_element(by=By.XPATH, value='/html/body/div[1]/div/strong')
    assert logout_message.text == "You are logged out"


@pytest.mark.parametrize('login, password', [
    ('TestUser', 'wrongpassword'),
    ('WrongUser', "password"),
    ('WrongUser', 'wrongpassword')])
def test_login_failure(browser_login, login, password):
    browser = browser_login[0]
    # Fill up the login form
    browser_login[1].send_keys(login)
    browser_login[2].send_keys(password)
    # Login failure
    browser.find_element(by=By.XPATH, value='/html/body/div/form/div[3]/div[2]/input').click()
    login_message = browser.find_element(by=By.XPATH, value='/html/body/div[1]/div/strong')
    assert login_message.text == "Logon failed, try aqain..."


@pytest.fixture()
def admin_logged(browser_login):
    browser = browser_login[0]
    # Fill up the login form
    browser_login[1].send_keys("admin")
    browser_login[2].send_keys("admin")
    # Login confirm
    browser.find_element(by=By.XPATH, value='/html/body/div/form/div[3]/div[2]/input').click()
    return browser


def test_user_delete(admin_logged):
    browser = admin_logged
    user_to_delete = "TestUser"
    def find_user_in_table(i = 1):
        while True:
            user = browser.find_element(by=By.XPATH, value=f'/html/body/div[2]/table/tbody/tr[{i}]/td[1]')
            if user.text == user_to_delete:
                return user, i
            i += 1

    # Open users table
    browser.find_element(by=By.XPATH, value='//*[@id="navbarDropdown"]').click()
    browser.find_element(by=By.XPATH, value='/html/body/nav/div/div/ul/li[4]/div/a[1]').click()
    # Check if the TestUser exists
    user, index = find_user_in_table()
    assert user.text == user_to_delete
    # Choose the TestUser to delete
    browser.find_element(by=By.XPATH, value=f'/html/body/div[2]/table/tbody/tr[{index}]/td[5]/a[2]').click()
    # Check if message is correct
    popup_message = browser.find_element(by=By.XPATH, value='//*[@id="idDeleteModalBody"]')
    assert popup_message.text == f"Delete user {user_to_delete}?"
    # Delete the chosen user
    browser.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[3]/form/button[2]').click()
    # Confirm it does not exist anymore
    with pytest.raises(StaleElementReferenceException):
        assert user.text
