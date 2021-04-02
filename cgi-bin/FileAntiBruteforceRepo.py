import json
import random
from datetime import datetime
import os
import sys

class FileAntiBruteforceRepo(object):
    """Класс репозитория подсчёта неудачных попыток авторизоваться для работы с файлом"""
    
    #Путь к файлу
    COUNTER_PATH = 'cgi-bin/counter.json'

    def __init__(self):
        """Конструктор класса репозитория подсчёта неудачных попыток авторизоваться"""
        #Создаётся файл для хранения если его нет
        try:
            with open(self.COUNTER_PATH, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.COUNTER_PATH, 'w+', encoding='utf-8') as f:
                json.dump({}, f)

    def get_all(self):
        with open(self.COUNTER_PATH, 'r', encoding='utf-8') as f:
            LoginFailedCounter = json.load(f)
        return LoginFailedCounter

    def update(self, ip, inc):
        counters = self.get_all()
        counters.setdefault(ip, {'count' : 0, 'datetime' : datetime.now().strftime("%d/%m/%Y %H:%M:%S")} )
        if inc:
            counters[ip]['count'] = counters[ip]['count'] + 1
        with open(self.COUNTER_PATH, 'w+', encoding='utf-8') as f:
            json.dump(counters, f)
        return counters[ip]['count']

    def checkTime(self, ip):
        counters = self.get_all()
        if ip in counters:
            c = counters[ip]['datetime']
            date_time_stored = datetime.strptime(counters[ip]['datetime'], "%d/%m/%Y %H:%M:%S")
            delta = datetime.now() - date_time_stored
            if delta.seconds > 60:
                return True
        return False

    def delete(self, ip):
        counters = self.get_all()
        if ip in counters:
            del counters[ip]
            with open(self.COUNTER_PATH, 'w+', encoding='utf-8') as f:
                json.dump(counters, f)
        return