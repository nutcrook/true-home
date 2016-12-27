from werkzeug.security import generate_password_hash, check_password_hash


class User(object):
    def __init__(self, name, email, password):
        self._name = name
        self._email = email
        self._password = generate_password_hash(password)
