import jwt
import datetime
from app.controllers.auth_token import SECRET_KEY, AuthTokenStatus


class AuthToken:

    def __init__(self, subject=None, duration=None, encoded_value=None):
        if subject:
            encoded_value, status = self.encoded_value_from_subject(subject, duration)
        elif encoded_value:
            subject, status = self.subject_from_encoded_token_value(encoded_value)

        self.subject = subject
        self.encoded_value = encoded_value
        self.status = status

    def encoded_value_from_subject(self, subject, duration):
        payload = {
            'exp': datetime.datetime.utcnow() + duration,
            'iat': datetime.datetime.utcnow(),
            'sub': subject
        }
        encrypted_value = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
        subject, status = self.subject_from_encoded_token_value(encrypted_value)
        return encrypted_value, status

    def subject_from_encoded_token_value(self, encoded_value):
        subject = None
        status = None
        try:
            subject = jwt.decode(encoded_value, SECRET_KEY)['sub']
            status = AuthTokenStatus.VALID
        except jwt.ExpiredSignatureError:
            status = AuthTokenStatus.EXPIRED
        except jwt.InvalidTokenError:
            status = AuthTokenStatus.INVALID

        return subject, status
