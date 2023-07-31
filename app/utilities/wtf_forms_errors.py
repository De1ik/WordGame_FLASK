from flask import flash

def error_checks(form):
    try:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', category='error')
    except:
        pass