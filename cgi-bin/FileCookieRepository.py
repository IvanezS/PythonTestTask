import json
import random
import time
import http.cookies
import os
import sys

class FileCookieRepository(object):
    """Класс репозитория пользователя для работы с файлом"""
    
    #Путь к файлу
    COOKIES_PATH = 'cgi-bin/cookies.json'

    def __init__(self):
        """Конструктор класса репозитория кук с файлом"""
        #Создаётся файл для хранения кук если его нет
        try:
            with open(self.COOKIES_PATH, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.COOKIES_PATH, 'w+', encoding='utf-8') as f:
                json.dump({}, f)

    
    
    def set_cookie(self, userlogin):
        """Записывает куку в файл. Возвращает созданную куку."""
        with open(self.COOKIES_PATH, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        cookie = str(time.time()) + str(random.randrange(10**14))  # Генерируем уникальную куку для пользователя
        cookies[cookie] = userlogin
        with open(self.COOKIES_PATH, 'w+', encoding='utf-8') as f:
            json.dump(cookies, f)
        return cookie
    
    def delete_cookie(self, cookie):
        """Записывает куку в файл. Возвращает созданную куку."""
        with open(self.COOKIES_PATH, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        del cookies[cookie]
        with open(self.COOKIES_PATH, 'w+', encoding='utf-8') as f:
            json.dump(cookies, f)
        return True

    def find_cookie(self, cookie):
        """По куке находит имя пользователя"""
        with open(self.COOKIES_PATH, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        return cookies.get(cookie)

    def get_session(self):
        cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
        session = cookie.get("session")
        if session is not None:
            session = session.value
        return session