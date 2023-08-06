from flask import session
from flask_login import current_user

from .set_word import set_word
from app import db



#number of letters

word_len = 5

word_history_lens = 5

def check_client_session(wd_len):
    global word_len
    word_len = wd_len
    #если пользователь первый раз - добавить его в сессии и запустить игру
    global_direct = direct_match = ' '.join(['_']*word_len)
    if 'user_game' not in session:
        session['user_game'] = True
        reset()
    return global_direct, direct_match


def reset():
   """Ресетит все данные"""
   print('RESET WAS DONE')
   session.pop('client_word', None)
   session['global_direct'] = ['_']*word_len
   session['global_indirect'] = list()
   session['word_history'] = [' ']*word_history_lens
   session['last_time_win'] = False
   session['attempt_number'] = 0
   session['find_word'] = set_word(word_len)
   print(f"FIND WORD = {session['find_word']}")

   return session['global_direct'], session['global_indirect'], session['word_history'], session['last_time_win']


def check_win(find_word, client_word):
    if session[f'last_time_win'] == True:
        reset()
    elif find_word==client_word:
        session[f'last_time_win']=True
        session[f'client_word'] = ''


def find_indirect_match(find_word, prev_ind, global_direct, indirect_match):
    #обьединяет прошлый индирект с настоящим и берет общее с копи фаинд ворд
    copy_f_w = find_word 
    for ind in range(word_len):
        if find_word[ind] == global_direct[ind]:
            copy_f_w = copy_f_w.replace(find_word[ind], '', 1)

    result = (set(prev_ind)|set(indirect_match))&set(copy_f_w)
    return result


def add_to_wordlist(client_word):
    """Если слово не равно последнему, то записываем его в общий список, возвращаем последние 5 слов"""
    try:
        if session['word_history'][-1] != client_word:
            session['word_history'].append(client_word)
    except:
        session['word_history'].append(client_word)
    return session['word_history'][-1:-6:-1]


def set_dir_match(client_word, find_word):
    """находим прямое вхождение и возвращаем, copy_find_word будет использоваться для поиска непрямого вхождения"""
    copy_find_word = find_word
    direct_match = ['_']*word_len
    for index in range(word_len):
        if find_word[index] == client_word[index]:
            # check
            direct_match[index] = client_word[index]
            session['global_direct'][index] = client_word[index]
            #----------------------------------------
            copy_find_word = copy_find_word.replace(client_word[index], '', 1)
    return copy_find_word, ' '.join(direct_match)


def word_finder(find_word, client_word):
    """соединяет функции и возвращает всю нужную информацию"""
    check_win(find_word=find_word, client_word=client_word)

    word_history = add_to_wordlist(client_word)

    copy_find_word, direct_match = set_dir_match(client_word =client_word, find_word=find_word)

    indirect_match = ' '.join(set(copy_find_word)&set(client_word))

    result_gl_indirect = set(find_indirect_match(find_word=find_word, 
                                               prev_ind=session['global_indirect'], 
                                               global_direct=session['global_direct'], 
                                               indirect_match=indirect_match))
    session['global_indirect'] = list(result_gl_indirect)

    
    return direct_match, indirect_match, ' '.join(session['global_direct']), ' '.join(session['global_indirect']), word_history