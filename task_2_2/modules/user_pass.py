from flask import session, flash
import hashlib
import binascii
import random
import string
from task_2_2.querries import DatabaseQuerries

db = DatabaseQuerries()

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
        # user_record = Users.query.filter(Users.name == self.user).first()
        user_record = db.get_user_by_name(user_name=self.user)
        if user_record != None and self.verify_password(user_record.password, self.password):
            return user_record
        else:
            self.user = None
            self.password = None
            return None

    def get_user_info(self):
        # user_info = Users.query.filter(Users.name == self.user).first()
        user_info = db.get_user_by_name(user_name=self.user)

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
