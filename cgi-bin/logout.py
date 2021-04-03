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
from JWT import JWT_token_tool

#Создаём экземпляры репозитория пользователей и кук для работы с файлом. Абстрагируемся от реализации методов работы в этом классе
user_repo = FileUserRepository() 
jwt = JWT_token_tool()

# Первичная инициализация
pattern = LoginView()

# Проверим токен и получим инфу из него (userId)
result = jwt.CheckJWTtoken()

# Получили userId, найдём по нему инфу о пользователе
if result is not False:
    temp_user = user_repo.getUserByUserId(result['userId'])
    if temp_user is not None:
        form = cgi.FieldStorage()
        action = form.getfirst("action", "")

        # Если пришли данные с формы
        if action == "logout":
            print('Set-cookie: JWTtoken={}'.format("0"))
            pattern = LoginView()
        else:
            pattern = SuccessLoginView()

# Выведем на экран
print(pattern)
