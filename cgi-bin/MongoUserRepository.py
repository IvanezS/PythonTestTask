from pymongo import MongoClient
from UserClass import User

class MongoUserRepository(object):
    """Класс репозитория пользователя для MongoDB"""

    def __init__(self):
        """Конструктор класса репозитория пользователя для MongoDB"""
        #Создаём соединение с БД
        try:
            mongoclient = MongoClient('localhost', 27017)
            print("Connected to MongoDB successfully!!!")
        except:  
            print("Could not connect to MongoDB")

        # Работаем с БД "database"
        db = mongoclient.database    

        # Создаём или подключается к коллекции пользователей "usercollection"
        self._users = db.usercollection
    
    
    def create(self, user):
        """Создать пользователя"""
        u = {
            'Birth': user.Birth,
            'HashedPassword': user.HashedPassword,
            'Name': user.Name,
            'SecondName' : user.SecondName
        }
        return self._users.insert_one(u)
        
  
    # Операции чтения
    def read_all(self):
        """Найти всех пользователей"""
        return self._users.find()
    
    def read_many(self, conditions):
        """Найти пользователей по условию"""
        return self._users.find(conditions)

    def find_by_name_and_password(self, name, password):
        """Найти пользователя по имени и паролю"""
        us = self._users.find_one({'Name': name, 'HashedPassword' : password})
        return us

    def getUserByUserId(self, userId):
        """Найти пользователя по userId"""
        if userId is None:
            raise TypeError
        usercollection = self._users.find_one({'_id': userId})
        user = User()
        return usercollection

    # Операции обновления
    def update(self, conditions, new_value):
        return self._users.update_one(conditions, new_value)
    
   
    # Delete operations
    def delete(self, condition):
        return self._users.delete_one(condition)
