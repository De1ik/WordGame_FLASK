from flask import Flask, render_template, request, session, redirect, flash , url_for
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from all_func import word_finder
import setting
from sql_models import email_db_check, sign_up_page, login_page, review_page, profile_get_stats, profile_persdata
from login_decorator import login_status



SECRET_KEY = os.getenv('SECRET_KEY')

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DATABASE')


app = Flask(__name__)
app.secret_key = SECRET_KEY
########################################################################
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///wordgame.db'
# db = SQLAlchemy(app)

app.config['dbconfig'] = {'host': DB_HOST,
                        'user': DB_USER,
                        'password': DB_PASSWORD,
                        'database': DATABASE}


@app.route('/main')
@app.route('/')
def main():
    print(app.config['dbconfig'])
    print(type(app.config['dbconfig']))
    return render_template('index.html')


@app.route('/game', methods=['POST', 'GET'])
def game():
    
    #ОБЫЧНЫЕ НА СЛУЧАЙ ЕСЛИ ЧЕЛОВЕК ТОЛЬКО ЗАШЕЛ
    global_direct = direct_match = ['_']*word_finder.word_len

    #СОЗДАНИЕ СЕССИИ
    #если нету его в сесиях - значит впервый раз - и тогда происхдит сброс\установка камонных данных в сесии
    user_id = request.remote_addr
    
    if session.get('logged_id'):
        print(session.get('logged_id'))
    else:
        print('user did not registrate')
    print(f'USER IP = {user_id}')
    if 'user_id' not in session:
         session['user_id'] = user_id
         word_finder.reset(user_id) #сброс\установка камонных данных в сесии
         return render_template('game.html', title = 'game', global_direct = ' '.join(global_direct), direct_match = ' '.join(direct_match)) 



    #func which will return word
    find_word = session.get(f'{user_id}-find_word')
    print(find_word)
    #--------------------------------------------------------------------------

    #ЕСЛИ ПОСТ ЗАПРОС ТО МЕНЯЕТСЯ КЛИЕНТСКОЕ СЛОВО
    if request.method == 'POST':  
        session[f'{user_id}-attempt_number'] = session.get(f'{user_id}-attempt_number') + 1
        session[f'{user_id}-client_word'] = request.form['word'].lower()
    try:
        client_word = session.get(f'{user_id}-client_word')
        direct_match, indirect_match, global_direct, global_indirect, word_history = word_finder.check_matching(find_word, client_word, user_id)
        return render_template('game.html', title = 'game',
                            find_word=find_word, client_word=client_word, word_history=word_history, direct_match= ' '.join(direct_match), indirect_match=indirect_match,
                            global_direct = ' '.join(global_direct), global_indirect= ' '.join(global_indirect), word_len=word_finder.word_len, attempt_number=session[f'{user_id}-attempt_number'])
    except:
        client_word = ''
        return render_template('game.html', title = 'game', global_direct = ' '.join(global_direct), direct_match = ' '.join(direct_match))


    #ПРОБУЕМ ДАТЬ ПРОШЛЫЙ ВАРИАНТ СЛОВА ЕСЛИ ЧЕЛОВЕК ПЕРЕКЛЮЧАЛСЯ МЕЖДУ СТРАНИЦАМИ, ЕСЛИ ОН ТОЛЬКО ПРИШЕЛ, ТО НИЧЕГО


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
        return render_template('profile.html',  title = 'profile', 
                            name=name, email = email,
                            numb_guessed=total_guessed, numb_attempt=total_attempt,
                            first_try=first_try, three_attemp=third_try,
                            max_attemp=max_attempt, average_attemp=average_attempt)
    except Exception as ex:
        print(ex)
        return 'some problems'


@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_id = request.remote_addr
        name = request.form['name']
        password = request.form['password']
        conf_password = request.form['conf_password']
        email = request.form['email']

        if email_db_check(db_config=app.config['dbconfig'], email=email):
            flash('email already registered', category='error')
        elif password != conf_password:
            flash('Passwords not equals!', category='error')
        else:
            sign_up_page(db_config=app.config['dbconfig'], name=name, email=email, password=generate_password_hash(password))
            return redirect('/login')
        
    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_id = request.remote_addr
        email = request.form['email']
        password = request.form['password']

        logid = login_page(db_config=app.config['dbconfig'], email=email, password=password)
        print(f'YOU CIURRENT LOG_ID: {logid}')
        if logid:
            session['logged_id'] = logid
            url = session.get('path') if session.get('path') else '/'
            return redirect(url)
        flash('wrong password or email', category='error')

    return render_template('login.html')


@app.route('/logout')
@login_status
def logout():
    user_id = request.remote_addr
    #session.pop(f'{user_id}-logid')
    session.pop('logged_id')
    return 'LOG OUT'


@app.errorhandler(404)
def eror_404(e):
    return render_template('404.html'), 404




if __name__ == '__main__':
    app.run(debug=True)