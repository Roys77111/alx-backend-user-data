#!/usr/bin/env python3
"""the basic auth class"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """basic authorization methods"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extracts the authorization code"""
        if (authorization_header is None or not
                isinstance(authorization_header, str)):
            return None
        if authorization_header[0:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decodes base 64 string"""
        if (base64_authorization_header and
                isinstance(base64_authorization_header, str)):
            try:
                encode = base64_authorization_header.encode('utf-8')
                base = base64.b64decode(encode)
                return base.decode('utf-8')
            except Exception:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """get user details from base64 decoded valuee"""
        decode_64 = decoded_base64_authorization_header
        if (decode_64 and isinstance(decode_64, str) and ":" in decode_64):
            result = decode_64.split(":", 1)
            return (result[0], result[1])
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        encoded = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(encoded)
        email, password = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(email, password)
        return user
