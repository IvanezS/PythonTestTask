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
            self.create(newUser.d, newUser.getUserId())

       
    def create(self, userDict, userId):
        """Регистриует пользователя. Возвращает True при успешной регистрации"""
        users = self.get_all()
        if userId in users:
           return False  # Такой пользователь существует
        with open(self.USER_PATH, 'w+', encoding='utf-8') as f:
            json.dump(userDict, f)
        return True
        
      # Операции чтения
    def get_all(self):
        """Найти всех пользователей"""
        with open(self.USER_PATH, 'r', encoding='utf-8') as f:
            users = json.load(f)
        return users
    
    def get_by_name_and_password(self, login, password):
        """Ищет пользователя по имени и паролю"""
        users = self.get_all()
        for userKey in users:
            if login in users[userKey]['login']:
                salt =  b64decode(users[userKey]['salt'].encode('utf-8')) # Get the salt
                key = b64decode(users[userKey]['key'].encode('utf-8')) # Get the correct key
                new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
                if key == new_key:
                    return userKey
        return None

    def getUserByUserId(self, userId):
        """Найти пользователя по userId"""
        if userId is None:
            raise TypeError
        users = self.get_all()
        x= users[userId]
        return x


