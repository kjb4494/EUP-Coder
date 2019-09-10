from django.shortcuts import render
from backend.json_response_helper import auth_error


def requires_login(func):
    def wrapper(*args, **kwargs):
        if not args[0].user.is_authenticated:
            res = render(args[0], 'errorPages/403.html')
            res.status_code = 403
            return res
        order = func(*args, **kwargs)
        return order

    return wrapper


def auth_req_api(func):
    def wrapper(*args, **kwargs):
        if not args[0].user.is_authenticated:
            return auth_error()
        order = func(*args, **kwargs)
        return order

    return wrapper
