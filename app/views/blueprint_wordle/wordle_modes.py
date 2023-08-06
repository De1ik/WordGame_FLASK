from flask import Blueprint, render_template, session, request
from flask_login import current_user


from app.wtf_forms import GameForm
from app.views.blueprint_wordle.wordle_utilites.wordle_finder import WordleFinder
from app.models import db
from app.models import Wordle5Letters, Wordle6Letters, Wordle7Letters
from .wordle_utilites.wordle_game_class import WordleGameTemp

wordle_index = Blueprint('wordle', __name__)
wordle_5_lt_bp = Blueprint('wordle-5-lt', __name__)
wordle_7_lt_bp = Blueprint('wordle-7-lt', __name__)
wordle_6_lt_bp = Blueprint('wordle-6-lt', __name__)

@wordle_5_lt_bp.route('/', methods=['GET', 'POST'])
def wordle():
    return 'all wordle games'



@wordle_5_lt_bp.route('/5-letters', methods=['GET', 'POST'])
def wordle_5_lt():
    #проверка первый раз пользователь зашел или нет
    wd_len = 5
    form = GameForm()
    game = WordleFinder(word_len=wd_len)

    #set new user
    if current_user.is_authenticated:
        
        user = Wordle5Letters.query.filter_by(user_id=current_user.user_id).first()
        if not user:     
            user = Wordle5Letters(user_id = current_user.user_id)
            db.session.add(user)
            db.session.commit()
    else:
        user = None

    print(f'USER {user}')

    wordle_game = WordleGameTemp(wd_len, form, game, user)
    all_data = wordle_game.main()
    if all_data:
        direct_match, indirect_match, global_direct, global_indirect, word_history, attempt_number, find_word, client_word = all_data
        return render_template('wordle.html', title = 'WORDLE', form=form, games='active',
                            word_len = wd_len, 
                            find_word = find_word, 
                            client_word = client_word,
                            word_history = word_history,
                            direct_match = direct_match, 
                            indirect_match = indirect_match,
                            global_direct = global_direct,
                            global_indirect = global_indirect,
                            attempt_number = attempt_number)
    
    return render_template('wordle.html', title = 'WORDLE', form=form, global_direct = game.direct_template, direct_match = game.direct_template, word_len = wd_len)




@wordle_6_lt_bp.route('/6-letters', methods=['GET', 'POST'])
def wordle_6_lt():
    #проверка первый раз пользователь зашел или нет
    wd_len = 6
    form = GameForm()
    game = WordleFinder(word_len=wd_len)

    #set new user
    if current_user.is_authenticated:
        user = Wordle6Letters.query.filter_by(user_id=current_user.user_id).first()
        if not user:     
            user = Wordle6Letters(user_id = current_user.user_id)
            db.session.add(user)
            db.session.commit()
    else:
        user = None

    wordle_game = WordleGameTemp(wd_len, form, game, user)
    all_data = wordle_game.main()
    if all_data:
        direct_match, indirect_match, global_direct, global_indirect, word_history, attempt_number, find_word, client_word = all_data
        return render_template('wordle.html', title = 'WORDLE', form=form, games='active',
                            word_len = wd_len, 
                            find_word = find_word, 
                            client_word = client_word,
                            word_history = word_history,
                            direct_match = direct_match, 
                            indirect_match = indirect_match,
                            global_direct = global_direct,
                            global_indirect = global_indirect,
                            attempt_number = attempt_number)
    
    return render_template('wordle.html', title = 'WORDLE', form=form, global_direct = game.direct_template, direct_match = game.direct_template, word_len = wd_len)





@wordle_7_lt_bp.route('/7-letters', methods=['GET', 'POST'])
def wordle_7_lt():
    #проверка первый раз пользователь зашел или нет
    wd_len = 7
    form = GameForm()
    game = WordleFinder(word_len=wd_len)

    #set new user
    if current_user.is_authenticated:
        user = Wordle7Letters.query.filter_by(user_id=current_user.user_id).first()
        if not user:     
            user = Wordle7Letters(user_id = current_user.user_id)
            db.session.add(user)
            db.session.commit()
    else:
        user = None

    wordle_game = WordleGameTemp(wd_len, form, game, user)
    all_data = wordle_game.main()
    if all_data:
        direct_match, indirect_match, global_direct, global_indirect, word_history, attempt_number, find_word, client_word = all_data
        return render_template('wordle.html', title = 'WORDLE', form=form, games='active',
                            word_len = wd_len, 
                            find_word = find_word, 
                            client_word = client_word,
                            word_history = word_history,
                            direct_match = direct_match, 
                            indirect_match = indirect_match,
                            global_direct = global_direct,
                            global_indirect = global_indirect,
                            attempt_number = attempt_number)
    
    return render_template('wordle.html', title = 'WORDLE', form=form, global_direct = game.direct_template, direct_match = game.direct_template, word_len = wd_len)

