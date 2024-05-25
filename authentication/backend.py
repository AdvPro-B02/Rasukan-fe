from django.conf import settings
from django.http import HttpRequest
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

import requests


class SpringBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, email: str = None, password: str = None, **kwargs):
        UserModel = get_user_model()
        resp = requests.post(f"{settings.AUTH_URL}/auth/login", data={"email": email, "password": password})
        body = resp.json()
        if resp.status_code != 200:
            return None
        
        user = UserModel(username=body["name"], id=body["id"], balance=body["balance"])
        request.COOKIES = dict(resp.cookies)
        return user
    

    def get_user(self, user_id: str):
        UserModel = get_user_model()
        resp = requests.get(f"{settings.AUTH_URL}/api/users/{user_id}")
        body = resp.json()
        if resp.status_code != 200:
            return None
        
        user = UserModel(username=body["name"], id=body["id"], balance=body["balance"])
        return user
