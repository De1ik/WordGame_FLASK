from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def login_status(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('profile'))
        return func(*args, **kwargs)
    return wrapper