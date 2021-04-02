from UserClass import User
import json
import random
import time
import hashlib#, uuid, os
from base64 import b64encode, b64decode


class FileUserRepository(object):
    """Класс репозитория пользователя для работы с файлом"""
    
    #Путь к файлу
    USER_PATH = 'cgi-bin/users.json'

    def __init__(self):
        """Конструктор класса репозитория пользователя с файлом"""
        #Создаётся файл для хранения пользователей если его нет
        try:
            with open(self.USER_PATH, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.USER_PATH, 'w+', encoding='utf-8') as f:
                json.dump({}, f)
        us = self.get_all()        
        if len(us) == 0:
            newUser=User("Vladimir", "1", "Vladimir", "Lenin", "2010-01-01")
            self.create(newUser.d)

    
    
    def create(self, user):
        """Регистриует пользователя. Возвращает True при успешной регистрации"""
        #if self.getUserByUserId(user.d[]):
        #    return False  # Такой пользователь существует
        with open(self.USER_PATH, 'w+', encoding='utf-8') as f:
            json.dump(user, f)
        return True
        
  
    # Операции чтения
    def get_all(self):
        """Найти всех пользователей"""
        with open(self.USER_PATH, 'r', encoding='utf-8') as f:
            users = json.load(f)
        return users
    

    def get_by_name_and_password(self, login, password):
        """Ищет пользователя по имени или по имени и паролю"""
        with open(self.USER_PATH, 'r', encoding='utf-8') as f:
            users = json.load(f)
            for clue in users.keys():
                if clue == login:
                    salt =  b64decode(users[login]['salt'].encode('utf-8')) # Get the salt
                    key = b64decode(users[login]['key'].encode('utf-8')) # Get the correct key
                    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
                    if key == new_key:
                        return True
        return False

    def getUserByUserLogin(self, login):
        """Найти пользователя по userId"""
        if login is None:
            raise TypeError
        with open(self.USER_PATH, 'r', encoding='utf-8') as f:
            users = json.load(f)
        #for user in users and  (userId == users[UserId])  
        x= users[login]
        return x


