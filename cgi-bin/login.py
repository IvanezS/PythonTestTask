#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def SuccessLoginView(username):
    return '''
            <!DOCTYPE HTML>
            <html>
            <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>АВТОРИЗАЦИЯ</title>
            <link rel="stylesheet" href="../static/css/styles.css" type="text/css">
            </head>
            <body>
                <div class="main">
                    <p class="sign" align="center">АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЯ</p>
                    <p class = "comment">Здравствуйте, %s! Вы успешно авторизовались</p>
                    <hr/>
                    
                    
                    <p align="center"><a class="info" href="/cgi-bin/user.py">Посмотреть информацию о себе</a></p>
                    <p> </p>
                    <p align="center"><a class="exit" href="/cgi-bin/logout.py">Выйти</a></p>
                </div>
            </body>
            </html>
    ''' % username

def LoginView(errorMessage, clientIP):
    return '''
    <!DOCTYPE HTML>
        <html>
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>АВТОРИЗАЦИЯ</title>
        <link rel="stylesheet" href="../static/css/styles.css" type="text/css">
        </head>
        <body>
            <div class="main">
            <p class="sign" align="center">АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЯ</p>
            <p class = "comment">Здравствуйте! Введите свои имя пользователя и пароль, чтобы получить доступ к данным</p>
            <p class = "comment">Ваш IP-адрес: %s</p>''' % clientIP +'''
            <hr/>
            <form class="form1" action="/cgi-bin/login.py" method = "POST">

                <input class="un" align="center" type="text" name="login" placeholder="Логин"/>
                <input class="pass" align="center" type="password" name="password" placeholder="Пароль"/>
                <input type="hidden" name="action" value="login">
                <input class="submit" align="center" type="submit" value = "Войти">
                <p class = "errorMessage">%s</p>
            </form>
            
            
            </div>
        </body>
        </html>
    ''' % errorMessage

import os
import cgi
import html
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from FileUserRepository import FileUserRepository
from FileAntiBruteforceRepo import FileAntiBruteforceRepo
from JWT import JWT_token_tool

#Создаём экземпляры репозитория пользователей и счётчиков для работы с файлом. Абстрагируемся от реализации методов работы в этом классе
user_repo = FileUserRepository() 
counter_repo = FileAntiBruteforceRepo() 
jwt = JWT_token_tool()

# Первичная инициализация
pattern =''

# Проверим токен и получим инфу из него (userId)
result = jwt.CheckJWTtoken()

# Получили userId, найдём по нему инфу о пользователе
if result is not False:
    temp_user = user_repo.getUserByUserId(result['userId'])
    if temp_user is not None:
        # Считаем, что авторизовались
        pattern = SuccessLoginView(temp_user['name'])
        # Обнулим счётчик попыток
        counter_repo.delete(os.environ["REMOTE_ADDR"])

# Если токен не прошёл валидацию или не проверялся
else:
    form = cgi.FieldStorage()
    action = form.getfirst("action", "")


    #Прошла ли 1 мин?
    if counter_repo.checkTime(os.environ["REMOTE_ADDR"]):
        # Обнулим счётчик попыток
        counter_repo.delete(os.environ["REMOTE_ADDR"])
   

    errorMessage = ''
    pattern = LoginView(errorMessage, os.environ["REMOTE_ADDR"])
    # Если пришли данные с формы
    if action == "login":
        
        if counter_repo.update(os.environ["REMOTE_ADDR"], False) < 4:

            login = form.getfirst("login", "")
            login = html.escape(login)
            password = form.getfirst("password", "")
            password = html.escape(password)

            # Проверка заполненности полей (лучше б, конечно, с фронта этим заниматься)
            if login == '' or password == '':
                errorMessage = 'Логин и пароль обязателены к заполнению'
                pattern = LoginView(errorMessage, os.environ["REMOTE_ADDR"])
            else:
                # Проверим, существует ли такой пользователь
                userId = user_repo.get_by_name_and_password(login, password)
                
                if userId is not None:

                    # Обновляем токен
                    cookie = jwt.CreateJWTtoken(userId)
                    print('Set-cookie: JWTtoken={}'.format(cookie))
                    
                    # Получаем пользователя
                    temp_user = user_repo.getUserByUserId(userId)
                    if temp_user is not None:
                        # То считаем, что авторизовались
                        pattern = SuccessLoginView(temp_user['name'])
                        # Обнулим счётчик попыток
                        counter_repo.delete(os.environ["REMOTE_ADDR"])
                else:
                    errorMessage = 'Не найден такой пользователь, осталось %s попыток войти' %  str(5 - counter_repo.update(os.environ["REMOTE_ADDR"], True))
                    pattern = LoginView(errorMessage, os.environ["REMOTE_ADDR"])
        else:
            errorMessage = 'Вы исчерпали попытки. Попробуйте через минуту через 1 мин'
            #Прошла ли 1 мин?
            if counter_repo.checkTime(os.environ["REMOTE_ADDR"]):
                counter_repo.delete(os.environ["REMOTE_ADDR"])
                errorMessage = 'Теперь можно повторно пройти авторизацию'
            pattern = LoginView(errorMessage, os.environ["REMOTE_ADDR"])

# Выведем на экран
print(pattern)

