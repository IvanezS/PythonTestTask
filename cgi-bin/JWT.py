import hashlib, hmac
from datetime import datetime, timedelta
from base64 import urlsafe_b64encode, urlsafe_b64decode
import json, os
import http.cookies

class JWT_token_tool:
    """Класс работы с токеном"""

    def get_session(self):
        """Получаем токен из куки"""
        cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
        session = cookie.get("JWTtoken")
        if session is not None:
            session = session.value
        return session

    def CreateJWTtoken(self, userid):
        """Создаём JWT токен и возвращаем его"""

        header = b'{"alg":"HS256","typ":"JWT"}'
        payload = json.dumps({"userId":userid, "exp":(datetime.now() + timedelta(seconds=90)).strftime("%d/%m/%Y %H:%M:%S")}).encode('utf-8')
        secretKey = b'SE'

        unsignedToken = urlsafe_b64encode(header) + b'.'+ urlsafe_b64encode(payload)
        signature = urlsafe_b64encode(hmac.new(secretKey, unsignedToken, hashlib.sha256).digest())

        token = unsignedToken + b'.'+ signature
        token = token.replace(b'=', b'')
        tokenStr = token.decode('utf-8')
        return tokenStr

    def CheckJWTtoken(self):
        """Проверяем JWT токен на правильность секрета и не закончился ли его срок.
        При успешной проверке возвращаем payload с userId и датой окончания токена.
        """

        # Получаем токен
        token = self.get_session()
        if token == "0" or token is None:
            return False

        header = b'{"alg":"HS256","typ":"JWT"}'
        secretKey = b'SE'

        # Декодируем токен
        strList = token.split(".")
        payloadCripted = (strList[1] + "==").encode('utf-8')
        signatureCripted = strList[2]

        payloadBytes = urlsafe_b64decode(payloadCripted)
        payloadStr = payloadBytes.decode('utf-8')
        payload = json.loads(payloadStr)
        
        unsignedToken = urlsafe_b64encode(header) + b'.'+ urlsafe_b64encode(payloadBytes)
        signature = urlsafe_b64encode(hmac.new(secretKey, unsignedToken, hashlib.sha256).digest())
        signature = signature.replace(b'=', b'')
        signature = signature.decode('utf-8')

        # Проверим подписи и срок действия токена
        if (signature == signatureCripted):
            if datetime.now() < datetime.strptime(payload['exp'], '%d/%m/%Y %H:%M:%S'):
                return payload
        return False 
            

