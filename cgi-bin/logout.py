#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def SuccessLoginView():
    print('''
            <!DOCTYPE HTML>
            <html>
            <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>ЗАКОНЧИТЬ СЕАНС</title>
            <link rel="stylesheet" href="../static/css/styles.css" type="text/css">
            </head>
            <body>
                <div class="main">
                    <p class="sign" align="center">ЗАКОНЧИТЬ СЕАНС</p>
                    <p class = "comment">Вы уверены, что хотите закончить сеанс?</p>
                    <hr />
                    <form action="/cgi-bin/logout.py" method = "POST">
                        <input type="hidden" name="action" value="logout">
                        <p align="center"><input class="exit" type="submit" value = "Выйти" /></p>
                    </form>
                    <p align="center"><a  class="info" href = "/cgi-bin/user.py">Отмена</a></p>
                </div>
            </body>
            </html>
    ''')

def LoginView():
    print('''
        <html>
            <head>
                <meta http-equiv="refresh" content="0;URL=http://localhost:8000/cgi-bin/login.py" />
            </head>
        </html>
    ''')
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
            LoginView()

        else:
            SuccessLoginView()
else:
    LoginView()

