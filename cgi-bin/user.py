#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def SuccessLoginView(user):
    return """
            <!DOCTYPE HTML>
            <html>
            <head>
            <meta charset="utf-8">
            <title>Login</title>
            </head>
            <body>
                <h1>ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ</h1>
                <hr/>
                <p>Имя: %s</p>""" % user['name']+"""
                <p>Фамилия: %s</p>""" % user['surname']+"""
                <p>День рождения: %s</p>""" % user['birth']+"""
                <p><a href="/cgi-bin/logout.py">Выйти</a></p>
                </body>
            </html>
    """

def LoginView():
    return '''
    <!DOCTYPE HTML>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Login</title>
        </head>
        <body>
            <h1>ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ</h1>
            <p>Информация недоступна. Необходимо пройти авторизацию - нажмите на кнопку Войти</p>
            <hr/>
            <p><a href="/cgi-bin/login.py">Войти</a></p>
        </body>
        </html>
    ''' 

import cgi
import html
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from FileUserRepository import FileUserRepository
from JWT import JWT_token_tool

#Создаём экземпляры репозитория пользователей и кук для работы с файлом. Абстрагируемся от реализации методов работы в этом классе
user_repo = FileUserRepository() 
jwt = JWT_token_tool()

# Первичная инициализация
pattern = LoginView()
result = False

# Проверим токен и получим инфу из него (userId)
result = jwt.CheckJWTtoken()

# Получили userId, найдём по нему инфу о пользователе
if result is not False:

    # Обновляем токен - типа обновляем срок действия токена
    cookie = jwt.CreateJWTtoken(result['userId'])
    print('Set-cookie: JWTtoken={}'.format(cookie))
    
    # Получаем пользователя
    temp_user = user_repo.getUserByUserId(result['userId'])
    if temp_user is not None:
        # То считаем, что авторизовались
        pattern = SuccessLoginView(temp_user)

# Выведем на экран
print(pattern)

