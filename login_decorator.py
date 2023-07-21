from flask import session, redirect, url_for, request
from functools import wraps

def login_status(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        if not session.get('logged_id'):
            session['path'] = request.path
            return redirect('/login')
        return func(*args, **kwargs)
    return wraper