from flask import session, redirect, request
from functools import wraps

def login_status(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        if not session.get('logged_id'):
            session['path'] = request.path
            return redirect('/login')
        return func(*args, **kwargs)
    return wraper

def login_stats(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        if session.get('logged_id'):
            return func(*args, **kwargs)
        return 'LOGIN STATS DECORATOR'
    return wraper