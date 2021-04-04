#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def SuccessLoginView(user):
    return """
            <!DOCTYPE HTML>
            <html>
            <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ</title>
            <link rel="stylesheet" href="../static/css/styles.css" type="text/css">
            </head>
            <body>
                <div class="main">
                    <p class="sign" align="center">ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ</p>
                    <p class = "comment">При простое более 1.5 минут сессия закончится</p>
                    <hr/>
                    <p class = "comment">Имя: %s</p>""" % user['name']+"""
                    <p class = "comment">Фамилия: %s</p>""" % user['surname']+"""
                    <p class = "comment">День рождения: %s</p>""" % user['birth']+"""
                    <p align="center"><a class="exit" href="/cgi-bin/logout.py">Выйти</a></p>
                </div>
            </body>
                
            </html>
    """

def LoginView():
    return '''
        <html>
            <head>
                <meta http-equiv="refresh" content="0;URL=http://localhost:8000/cgi-bin/login.py" />
            </head>
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

