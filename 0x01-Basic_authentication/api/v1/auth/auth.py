#!/usr/bin/env python3
"""API authentication class"""
import flask
import json
from flask import request
from typing import List, TypeVar


class Auth():
    """Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if authorization is required"""
        check = path
        if path is None:
            return True
        if excluded_paths is None or []:
            return True
        if path[-1] != "/":
            check += "/"
        if check in excluded_paths or path in excluded_paths:
            return False

        for i in excluded_paths:
            if i[len(i) - 1] != '*':
                return False
            else:
                if i[:-1] == path[:len(i) - 1]:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """create header with authorization details"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """get the current user """
        return None
