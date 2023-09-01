from flask import session
from flask_login import current_user

from ....utilities.set_word import set_word
from ....utilities.delate_all_sessions import delete_sessions




class WordleFinder:
    def __init__(self, word_len):
        self._word_len = word_len
        self._word_history_lens = 5
        self.direct_template = ' '.join(['_'] * self._word_len)


    def reset(self):
        """Reset all data after win game"""
        session.pop('client_word', None)
        session['global_direct'] = ['_']*self._word_len
        session['global_indirect'] = list()
        session['word_history'] = [' ']*self._word_history_lens
        session['last_time_win'] = False
        session['attempt_number'] = 0
        session['find_word'] = set_word(self._word_len)
        print('RESET WAS DONE')
        print(f"FIND WORD = {session['find_word']}")


    def db_load_info(self, user):
        """load data from db if person logged in"""
        session['find_word'] = user.find_word
        session['global_direct'] = user.global_direct.split()
        session['global_indirect'] = user.global_indirect.split()
        session['word_history'] = user.word_list.split()
        session['attempt_number'] = user.attempts
        session['last_time_win'] = user.last_win     
        session['client_word'] = user.client_word
        session['indirect_match'] = user.indirect_match.split()
        session['direct_match'] = user.direct_match.split()


    def save_state_db(self, user, client_word, find_word, indirect_match, direct_match):
        """try update personal wordle info"""
        if current_user.is_authenticated:
            try:
                # user = Wordle6Letters.query.filter_by(user_id=current_user.user_id).first()
                result = user.update_wordle(client_word, 
                                    find_word, 
                                    ' '.join(session['global_direct']), 
                                    ' '.join(session['global_indirect']), 
                                    ' '.join(session['word_history']), 
                                    session['attempt_number'], 
                                    ' '.join(indirect_match), 
                                    ' '.join(direct_match),
                                    session['last_time_win'])
                return result
            except Exception as ex:
                print(ex)
                return False


    def check_win(self, find_word, client_word):
        """checking if the last player game was win game or if this game is win game"""
        if session[f'last_time_win'] == True:
            self.reset()
        elif find_word==client_word:
            session[f'last_time_win']=True
            session[f'client_word'] = ''


    def find_indirect_match(self, find_word, prev_ind, global_direct, indirect_match):
        """unite last global indirect with current inderect_match"""
        copy_f_w = find_word 
        for ind in range(self._word_len):
            if find_word[ind] == global_direct[ind]:
                copy_f_w = copy_f_w.replace(find_word[ind], '', 1)

        result = (set(prev_ind)|set(indirect_match))&set(copy_f_w)
        return result


    def add_to_wordlist(self, client_word):
        """if current word != current word then append it into wordlist, return just 5 last words"""
        try:
            if session['word_history'][-1] != client_word:
                session['word_history'].append(client_word)
        except:
            session['word_history'].append(client_word)
        return session['word_history'][-1:-6:-1]


    def set_dir_match(self, client_word, find_word):
        """Find the direct match and return it, copy_find_word will use for searching indirect match"""
        copy_find_word = find_word
        direct_match = ['_']*self._word_len
        for index in range(self._word_len):
            if find_word[index] == client_word[index]:
                direct_match[index] = client_word[index]
                session['global_direct'][index] = client_word[index]
                copy_find_word = copy_find_word.replace(client_word[index], '', 1)
        return copy_find_word, ' '.join(direct_match)


    def word_finder(self, client_word, find_word, user):
        """unite all function and return information for html"""

        self.check_win(find_word=find_word, client_word=client_word)

        word_history = self.add_to_wordlist(client_word)

        copy_find_word, direct_match = self.set_dir_match(client_word = client_word, find_word = find_word)

        indirect_match = ' '.join(set(copy_find_word)&set(client_word))

        result_gl_indirect = set(self.find_indirect_match(find_word=find_word, 
                                                prev_ind=session['global_indirect'], 
                                                global_direct=session['global_direct'], 
                                                indirect_match=indirect_match))
        session['global_indirect'] = list(result_gl_indirect)

        global_direct = ' '.join(session['global_direct'])
        global_indirect = ' '.join(session['global_indirect'])
        attempt_number = session['attempt_number']

        #save into db
        if current_user.is_authenticated:
            # if happened some troubles with updating in db => return false
            result = self.save_state_db(user, client_word, find_word, indirect_match, direct_match)
            delete_sessions() if result else None

        
        return direct_match, indirect_match, global_direct, global_indirect, word_history, attempt_number

















































































































    # def reset(self):
    #     """Resets all data"""
    #     # print('RESET WAS DONE')
    #     # self.global_direct = ['_'] * self._word_len
    #     # self.global_indirect = set()
    #     # self.word_history = [' '] * self._word_history_lens
    #     # self.last_time_win = False
    #     # self.attempt_number = 0
    #     # self.find_word = set_word(self._word_len)

    #     session.pop('client_word', None)
    #     session['global_direct'] = ['_']*self._word_len
    #     session['global_indirect'] = list()
    #     session['word_history'] = [' ']*self._word_history_lens
    #     session['last_time_win'] = False
    #     session['attempt_number'] = 0
    #     session['find_word'] = set_word(self._word_len)
    #     print(f"FIND WORD = {session['find_word']}")

    #     return session['global_direct'], session['global_indirect'], session['word_history'], session['last_time_win']


    # def check_win(self):
    #     if self.last_time_win:
    #         self.reset()
    #     elif self.find_word == self.client_word:
    #         self.last_time_win = True
    #         session['client_word'] = ''


    # def find_indirect_match(self, prev_ind): # global_direct, indirect_match
    #     # Combines the previous indirect with the current one and takes the common with the copy of find_word
    #     copy_f_w = self.find_word
    #     for ind in range(self._word_len):
    #         if self.find_word[ind] == self.global_direct[ind]:
    #             copy_f_w = copy_f_w.replace(self.find_word[ind], '', 1)

    #     result = (set(prev_ind) | set(self.indirect_match)) & set(copy_f_w)
    #     return result


    # def add_to_wordlist(self):
    #     """If the word is not equal to the last one, append it to the general list, return the last 5 words"""
    #     if self.word_history[-1] != self.client_word:
    #         self.word_history.append(self.client_word)
    #     return self.word_history[-1:-6:-1]


    # def set_dir_match(self):
    #     """Finds direct matches and returns the copy of find_word to search for indirect matches"""
    #     copy_find_word = self.find_word
    #     self.direct_match = ['_'] * self._word_len
    #     for index in range(self._word_len):
    #         if self.find_word[index] == self.client_word[index]:
    #             self.direct_match[index] = self.client_word[index]
    #             self.global_direct[index] = self.client_word[index]
    #             copy_find_word = copy_find_word[:index] + copy_find_word[index + 1:]
    #     return copy_find_word, ''.join(self.direct_match)


    # def word_finder(self, client_word):
    #     """Combines functions and returns all the necessary information"""
    #     if current_user.is_authenticated:
    #         self.db_load_info()

    #         # self.client_word
    #         # self.find_word
    #         # self.global_direct
    #         # self.global_indirect
    #         # self.word_history
    #         # self.attempt_number




            
    #     self.client_word = client_word
    #     self.check_win()
    #     self.word_history = self.add_to_wordlist()
    #     copy_find_word, self.direct_match = self.set_dir_match()
    #     self.indirect_match = ''.join(set(copy_find_word) & set(client_word))
    #     result_gl_indirect = self.find_indirect_match(prev_ind=self.global_indirect)
    #     self.global_indirect = list(result_gl_indirect)
        
    #     #save into db
    #     if current_user.is_authenticated:
    #         self.save_state_db()
    #     else:
    #         pass
    #     return self.direct_match, self.indirect_match, ''.join(self.global_direct), ' '.join(self.global_indirect), self.word_history, self.attempt_number, self.find_word



    # def db_load_info(self, user):
    #     self.client_word = user.client_word
    #     self.find_word = user.find_word
    #     self.global_direct = user.global_direct
    #     self.global_indirect = user.global_indirect
    #     self.word_history = user.word_list
    #     self.attempt_number = user.attempts
    #     self.indirect_match = user.indirect_match
    #     self.direct_match = user.direct_match


    # def save_state_db(self, user):
    #     user = Wordle6Letters.query.filter_by(user_id=current_user.user_id).first()
    #     user.update_user_stats(self.client_word, self.find_word, self.global_direct, self.global_indirect, self.word_history, self.attempt_number, self.indirect_match, self.direct_match)
        

    #     print('SAVING INTO DB')




























    # def to_json(self):
    #     # Преобразование атрибутов класса в словарь
    #     return {
    #         "_word_len": self._word_len,
    #         "_word_history_lens": self._word_history_lens,
    #         "attempt_number": self.attempt_number,
    #         "last_time_win": self.last_time_win,
    #         "direct_match": self.direct_match,
    #         "global_direct": self.global_direct,
    #         "global_indirect": self.global_indirect,
    #         "client_word": self.client_word,
    #         "find_word": self.find_word,

    #         # Добавьте остальные атрибуты, которые хотите сохранить
    #         # ...
    #     }

    # @classmethod
    # def from_json(cls, data):
    #     # Создание объекта класса из словаря
    #     word_finder = cls(data["_word_len"])
    #     word_finder._word_history_lens = data["_word_history_lens"]
    #     word_finder.attempt_number = data["attempt_number"]
    #     word_finder.last_time_win = data["last_time_win"]
    #     word_finder.direct_match = data["direct_match"]
    #     word_finder.global_direct = data["global_direct"]
    #     word_finder.global_indirect = data["global_indirect"]
    #     word_finder.find_word = data["find_word"]
    #     word_finder.client_word = data["client_word"]

    #     # Добавьте остальные атрибуты, которые хотите восстановить
    #     # ...
    #     return word_finder