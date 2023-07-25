from flask import Flask, render_template, request, session, redirect, flash , url_for, make_response
from werkzeug.security import generate_password_hash
from datetime import timedelta
import os

from all_func import word_finder, email_validation
import setting
from sql_models import email_db_check, sign_up_page, login_page, review_page, profile_get_stats, profile_persdata
from login_decorator import login_status
from wtf_forms import LoginForm, SignUpForm



SECRET_KEY = os.getenv('SECRET_KEY')

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DATABASE')


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['dbconfig'] = {'host': DB_HOST,
                        'user': DB_USER,
                        'password': DB_PASSWORD,
                        'database': DATABASE,
                        'charset':'utf8mb4'}


@app.before_request
def make_session_permanent():
    session.permanent = True
    if 'checkbox' in session:
        print('CHECBOX TRUE')
        app.permanent_session_lifetime = timedelta(days=3)
    else:
        app.permanent_session_lifetime = timedelta(minutes=15)



@app.route('/main')
@app.route('/')
def main():
    return render_template('index.html')


@app.route('/game', methods=['POST', 'GET'])
def game():
    #проверка первый раз пользователь зашел или нет
    global_direct, direct_match = word_finder.check_client_session()

    if request.method == 'POST':
        #если пост - значит пользователь что то написал -> нужно обновить количество попыток и взять клиентское слово, обновляет стату если зареган
        client_word = request.form['word'].lower()
        word_finder.update_all_info(client_word=client_word, db_config=app.config.get('dbconfig'), user_id=session.get('logged_id'))
    try:
        #Даже если гет запрос, но человек до этого уже играл -> вернуть прошлое слово
        client_word = session['client_word']
        find_word = session.get('find_word')
        direct_match, indirect_match, global_direct, global_indirect, word_history = word_finder.word_finder(find_word, client_word)
        return render_template('game.html', title = 'game',
                        find_word=find_word, 
                        client_word=client_word, 
                        word_history=word_history, 
                        direct_match= direct_match, 
                        indirect_match=indirect_match,
                        global_direct = global_direct,
                        global_indirect= global_indirect, 
                        word_len=word_finder.word_len, 
                        attempt_number=session['attempt_number'])
    except:
        #Если не получается то базовый вывод
        #client_word = ''
        return render_template('game.html', title = 'game', global_direct = global_direct, direct_match = direct_match)


@app.route('/rules')
def rules():
    return render_template('rules.html')


@app.route('/reviews', methods=['POST', 'GET'])
@login_status
def reviews():
    if request.method == 'POST':
        review = request.form['review']
        result = review_page(db_config=app.config['dbconfig'], user_id=session['logged_id'], review=review)
        if result:
            flash('Review was send. Thanks!', category='success')
        else:
            flash('Something went wrong :(', category='error')
        return redirect('/reviews')

    return render_template('reviews.html', title = 'reviews')


@app.route('/profile')
@login_status
def profile():
    try:
        total_guessed, total_attempt, first_try, third_try, average_attempt, max_attempt = profile_get_stats(db_config=app.config['dbconfig'], user_id=session['logged_id'])
        name, email = profile_persdata(db_config=app.config['dbconfig'], user_id=session['logged_id'])
        return render_template('profile.html', title = 'profile',
                            name=name, email = email,
                            numb_guessed=total_guessed, numb_attempt=total_attempt,
                            first_try=first_try, three_attemp=third_try,
                            max_attemp=max_attempt, average_attemp=average_attempt)
    except Exception as ex:
        print(ex)
        return 'some problems'
    


@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        name = form.name.data
        password = form.psw.data
        conf_password = form.psw_confirm.data
        email = form.email.data

        if not email_validation.valid_email(email):
            flash('email is not valid', category='error')
        elif email_db_check(db_config=app.config['dbconfig'], email=email):
            flash('email already registered', category='error')
        elif password != conf_password:
            flash('Passwords not equals!', category='error')
        else:
            sign_up_page(db_config=app.config['dbconfig'], name=name, email=email, password=generate_password_hash(password))
            return redirect('/login')
        
    return render_template('signup.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.psw.data
        checkbox_value = form.remember.data

        logid = login_page(db_config=app.config['dbconfig'], email=email, password=password)
        print(f'YOUR CURRENT LOG_ID: {logid}')
        if logid:
            if checkbox_value:
                session['checkbox'] = True
            session['logged_id'] = logid
            url = session.get('path') if session.get('path') else '/'
            print('EVERYTHING IS FINE')
            return redirect(url)
        flash('wrong password or email', category='error')

    return render_template('login.html', form=form)





    if request.method == 'POST':
        # user_id = request.remote_addr
        email = request.form.get('email')
        password = request.form.get('password')
        checkbox_value = request.form.get('checkbox')

        logid = login_page(db_config=app.config['dbconfig'], email=email, password=password)
        print(f'YOUR CURRENT LOG_ID: {logid}')
        if logid:
            if checkbox_value:
                session['checkbox'] = True
            session['logged_id'] = logid
            url = session.get('path') if session.get('path') else '/'
            return redirect(url)
        flash('wrong password or email', category='error')

    return render_template('login.html')


@app.route('/logout', methods=['POST', 'GET'])
@login_status
def logout():
    if request.method == 'POST':
        res = request.form.get('logout')
        print(f'RES {res}')
        if res == 'Yes':
            session.clear()
            return redirect('/login')
        return redirect('/profile')
    return render_template('logout.html')


@app.errorhandler(404)
def eror_404(e):
    return render_template('404.html'), 404




if __name__ == '__main__':
    app.run(debug=True)