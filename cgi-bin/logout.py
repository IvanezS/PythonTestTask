#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def SuccessLoginView():
    return '''
            <!DOCTYPE HTML>
            <html>
            <head>
            <meta charset="utf-8">
            <title>Login</title>
            </head>
            <body>
                <h1>ЗАКОНЧИТЬ СЕАНС</h1>
                <hr />
                <p>Нажмите для подтверждения выхода на кнопку</p>
                <form action="/cgi-bin/logout.py" method = "POST">
                    <input type="hidden" name="action" value="logout">
                    <p><input type="submit" value = "Выйти" /><p>
                </form>
                <a href = "/cgi-bin/user.py">Перейти к информации о пользователе</a>
            </body>
            </html>
    '''

def LoginView():
    return '''
    <!DOCTYPE HTML>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Login</title>
        </head>
        <body>
            <h1>ЗАКОНЧИТЬ СЕАНС</h1>
            <p>Вы не авторизированы! </p>
            <hr/>
            <a href = "/cgi-bin/login.py">Перейти к странице авторизации</a>
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
        form = cgi.FieldStorage()
        action = form.getfirst("action", "")

        # Если пришли данные с формы
        if action == "logout":
            cookie = cookie_repo.set_cookie(userlogin)
            print('Set-cookie: session={}'.format(cookie))
            cookie_repo.delete_cookie(cookie)
            pattern = LoginView()

        else:
            pattern = SuccessLoginView()

# Если логин не найден или пользователь по логину не найден
if userlogin is None or temp_user is None:
    pattern = LoginView()

# Выведем на экран
print(pattern)
