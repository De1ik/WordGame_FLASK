from all_func import set_word
from flask import session

#number of letters
word_len = 6
word_history_lens = 6

def reset(user_id):
   session[f'{user_id}-global_direct'] = ['_']*word_len
   session[f'{user_id}-global_indirect'] = list()
   session[f'{user_id}-word_history'] = [' ']*word_history_lens
   session[f'{user_id}-last_time_win'] = False
   session[f'{user_id}-attempt_number'] = 0
   session[f'{user_id}-find_word'] = set_word.set_6_word().lower()

   return session[f'{user_id}-global_direct'], session[f'{user_id}-global_indirect'],session[f'{user_id}-word_history'], session[f'{user_id}-last_time_win']

# проверяет выиграш ли последняя игра => ресет и меня
def check_win(user_id):
    if session[f'{user_id}-last_time_win'] == True:
        reset(user_id)


def find_indirect_match(find_word, prev_ind, global_direct, indirect_match):
    #обьединяет прошлый индирект с настоящим и берет общее с копи фаинд ворд
    copy_f_w = find_word 
    for ind in range(word_len):
        if find_word[ind] == global_direct[ind]:
            copy_f_w = copy_f_w.replace(find_word[ind], '', 1)

    result = (set(prev_ind)|set(indirect_match))&set(copy_f_w)
    return result


def check_matching(find_word, client_word, user_id):
# -------------------МОЖНО ВЫНЕСТИ В НОВУЮ ФУНКЦИЮ--------------------------

    # проверяет была ли прошлая игра победной - если да, то сбросс результата
    check_win(user_id)


    if find_word==client_word:
        session[f'{user_id}-last_time_win']=True
        session[f'{user_id}-client_word'] = ''


#---------------------------------------------------------------------------
    #добавляем в общий список наши слова
    try:
        if session[f'{user_id}-word_history'][-1] != client_word:
            session[f'{user_id}-word_history'].append(client_word)
    except:
        session[f'{user_id}-word_history'].append(client_word)

    copy_find_word = find_word
    direct_match = ['_']*word_len


    for index in range(word_len):
        if find_word[index] == client_word[index]:
            # check
            direct_match[index] = client_word[index]
            session[f'{user_id}-global_direct'][index] = client_word[index]
            #----------------------------------------
            copy_find_word = copy_find_word.replace(client_word[index], '', 1)

    indirect_match = set(copy_find_word)&set(client_word)
    
    result_gl_direct = set(find_indirect_match(find_word=find_word, prev_ind=session[f'{user_id}-global_indirect'], global_direct=session[f'{user_id}-global_direct'], indirect_match=indirect_match))
    session[f'{user_id}-global_indirect'] = list(result_gl_direct)
    
    word_history = session[f'{user_id}-word_history'][-1:-6:-1]
    indirect_match = ' '.join(indirect_match)
    
    return direct_match, indirect_match, session[f'{user_id}-global_direct'], session[f'{user_id}-global_indirect'], word_history


