import hashlib, uuid, os
from base64 import b64encode

class User:
    """Класс пользователя"""

    def __init__(self, login, password, name, surname, birth):
        """Конструктор класса пользователя"""
        self.d={}
        salt = os.urandom(64) # A new salt for this user
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        self.d[login] = { # Store the salt and key
            'salt': b64encode(salt).decode('utf-8'),
            'key': b64encode(key).decode('utf-8'),
            'userid' : b64encode(uuid.uuid4().bytes).decode('utf-8'),
            'name' : name,
            'surname' : surname,
            'birth' : birth
        }

