from applications import app, login_manager, db, cashe


from flask import render_template, request, redirect, flash , url_for
from flask_login import logout_user, login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import timedelta, datetime

from .models import UserInfo, Reviews, WordleStatistics
from .wtf_forms import LoginForm, SignUpForm, ReviewsForm, UpdateInfoForm

from .utilities import word_finder

from .utilities.wtf_forms_errors import error_checks
from .utilities.login_status import login_status
from .utilities.delate_all_sessions import delete_sessions



# @app.before_request
# def make_session_permanent():
#     session.permanent = True
#     if 'checkbox' in session:
#         app.permanent_session_lifetime = timedelta(days=3)
#     else:
#         app.permanent_session_lifetime = timedelta(minutes=15)




@login_manager.user_loader
def load_user(id):
    return UserInfo.query.get(int(id))


@app.route('/')
@cashe.cached(timeout=300)
def index():
    return render_template('index.html', index='active')


@app.route('/games', methods=['POST', 'GET'])
@cashe.cached(timeout=300)
def games():
    return render_template('games.html', games='active')


@app.route('/rules')
@cashe.cached(timeout=300)
def rules():
    return render_template('rules.html', rules='active')


@app.route('/wordle-rules')
@cashe.cached(timeout=300)
def wordle_rules():
    return render_template('wordle-rules.html', rules='active')


@app.route('/review', methods=['POST', 'GET'])
@cashe.cached(timeout=300)
@login_required
def review():
    form = ReviewsForm()

    if form.validate_on_submit():
        try:
            review = form.review.data
            user = Reviews(user_id=current_user.user_id, review=review)
            db.session.add(user)
            db.session.commit()
            flash('Review was send. Thanks!', category='success')
        except Exception as ex:
            flash('Something went wrong :(', category='error')
        return redirect(url_for('review'))

    return render_template('review.html', title = 'Review', review='active', form=form)


@app.route('/profile')
@cashe.cached(timeout=15)
@login_required
def profile():
    try:
        stats = WordleStatistics.query.filter_by(user_id=current_user.user_id).first()
        return render_template('profile.html', title = 'Profile', profile='active',
                            numb_guessed=stats.total_guessed, numb_attempt=stats.total_attempt,
                            first_try=stats.first_try, three_attemp=stats.third_try,
                            max_attempt=stats.max_attempt, average_attemp=stats.average_attempt,
                            wd_len_5 = stats.wd_len_5, wd_len_6 = stats.wd_len_6, wd_len_7 = stats.wd_len_7,
                            wd_skill_lvl = stats.wd_skill_lvl)
    except Exception as ex:
        print(ex)
        return redirect(url_for('index'))


@app.route('/update-info', methods=['POST', 'GET'])
@login_required
def update_profile_info():
    form = UpdateInfoForm()
    email = form.email.data

    if form.validate_on_submit():
        user = UserInfo.query.filter_by(email=email).first()
        if user and current_user.email != email:
            flash('email already registered', category='error')
        else:
            current_user.name = form.name.data
            current_user.email = email
            db.session.commit()
            return redirect(url_for('profile'))
    else:
        error_checks(form)
        
    return render_template('update_profile_info.html', form=form)


@app.route('/sign-up', methods=['GET', 'POST'])
@cashe.cached(timeout=300)
@login_status
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        name = form.name.data
        password = generate_password_hash(form.psw.data)
        email = form.email.data

        user = UserInfo.query.filter_by(email=email).first()
        if user:
            flash('email already registered', category='error')
        else:
            user = UserInfo(name=name, email=email, password=password)
            db.session.add(user)
            user = UserInfo.query.filter_by(email=user.email).first()
            stats = WordleStatistics(user_id=user.user_id)
            db.session.add(stats)
            db.session.commit()
            return redirect(url_for('login'))
    else:
        error_checks(form)
        
    return render_template('signup.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
@cashe.cached(timeout=300)
@login_status
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        psw_cl = form.psw.data
        checkbox_value = form.remember.data

        user = UserInfo.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, psw_cl):
            
            print(f'USER ID {user.user_id}')
            login_user(user, remember=checkbox_value)
            next_page = request.args.get('next') or url_for('index')
            delete_sessions()
            return redirect(next_page)

        flash('wrong password or email', category='error')
    else:
        error_checks(form)

    return render_template('login.html', form=form)



@app.route('/logout', methods=['POST', 'GET'])
@cashe.cached(timeout=300)
@login_required
def logout():
    return render_template('logout.html')


@app.route('/logout-confirm', methods=['POST', 'GET'])
@cashe.cached(timeout=300)
@login_required
def logout_confirm():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
@cashe.cached(timeout=300)
def eror_404(e):
    return render_template('404.html'), 404
