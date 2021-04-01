#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def SuccessLoginView(user):
    x= """
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
    return x

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
from FileCookieRepository import FileCookieRepository

#Создаём экземпляры репозитория пользователей и кук для работы с файлом. Абстрагируемся от реализации методов работы в этом классе
user_repo = FileUserRepository() 
cookie_repo = FileCookieRepository() 

session = cookie_repo.get_session()

temp_user ={}
pattern =''''''

# Ищем логин пользователя по переданной куке
userlogin = cookie_repo.find_cookie(session)  

# Если логин найден, найдём по нему инфу о пользователе
if userlogin is not None:
    temp_user = user_repo.getUserByUserLogin(userlogin)
    if temp_user is not None:
        # То считаем, что авторизовались
        pattern = SuccessLoginView(temp_user)

# Если логин не найден или пользователь по логину не найден
if userlogin is None or temp_user is None:
    pattern = LoginView()


# Выведем на экран
print(pattern)

