#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def SuccessLoginView(username):
    return '''
            <!DOCTYPE HTML>
            <html>
            <head>
            <meta charset="utf-8">
            <title>Login</title>
            </head>
            <body>
                <h1>АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЯ</h1>
                <p>Здравствуйте, %s! Вы успешно авторизовались</p>
                <hr/>
                <p><a href="/cgi-bin/logout.py">Выйти</a></p>
                <p><a href="/cgi-bin/user.py">Посмотреть информацию о себе</a></p>
            </body>
            </html>
    ''' % username

def LoginView(errorMessage):
    return '''
    <!DOCTYPE HTML>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Login</title>
        </head>
        <body>
            <h1>АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЯ</h1>
            <p>Здравствуйте! Введите свои имя пользователя и пароль, чтобы получить доступ к данным</p>
            <hr/>
            <form action="/cgi-bin/login.py" method = "POST">

                <p>Логин:</p>
                <p><input type="text" name="login" /></p>
                <p>Пароль:</p>
                <p><input type="password" name="password" /></p>

                <input type="hidden" name="action" value="login">
                <p><input type="submit"/><p>
            </form>
            <font size="2" color="red">
                %s
            </font>

        </body>
        </html>
    ''' % errorMessage

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
        pattern = SuccessLoginView(temp_user['name'])

# Если логин не найден или пользователь по логину не найден
if userlogin is None or temp_user is None:


    form = cgi.FieldStorage()
    action = form.getfirst("action", "")

    errorMessage = ''

    # Если пришли данные с формы
    if action == "login":
        
        login = form.getfirst("login", "")
        login = html.escape(login)
        password = form.getfirst("password", "")
        password = html.escape(password)

        # Проверим, существует ли такой пользователь
        us = user_repo.get_by_name_and_password(login, password)
        
        if us:
            cookie = cookie_repo.set_cookie(login)
            print('Set-cookie: session={}'.format(cookie))
            temp_user = user_repo.getUserByUserLogin(login)
            if temp_user is not None:
                # То считаем, что авторизовались
                pattern = SuccessLoginView(temp_user['name'])
        else:
            errorMessage = 'Не найден такой пользователь'
            
            pattern = LoginView(errorMessage)
    else:
        pattern = LoginView(errorMessage)


# Выведем на экран
print(pattern)

