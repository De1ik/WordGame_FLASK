from flask import session, request
from flask_login import current_user


from applications.models import WordleStatistics
from applications.utilities.wtf_forms_errors import error_checks



class WordleGameTemp:
    def __init__(self, word_len, form, game, user) -> None:
        self.word_len = word_len
        self.form = form
        self.game = game
        self.user = user


    def load_data(self):
        if current_user.is_authenticated and self.user.last_win == False:
            self.game.db_load_info(self.user)
        elif request.method == 'GET':
            self.game.reset()

    
    def post_request(self):
        if self.form.validate_on_submit():
            if self.form.validate():

                client_word = self.form.word.data.lower()
                #update client word and count attempts
                session['attempt_number'] = session['attempt_number'] + 1
                session['client_word'] = client_word

                #update WordleStatistics
                if current_user.is_authenticated:
                    try:
                        user = WordleStatistics.query.filter_by(user_id=current_user.user_id).first()
                        print(f'WD LEN {self.word_len}')
                        user.update_user_stats(
                            client_word=session.get('client_word'),
                            find_word=session.get('find_word'),
                            attempt_number=session.get('attempt_number'),
                            wd_len = self.word_len)
                    except Exception as ex:
                        print(ex) 
        else:
            error_checks(self.form)


    def data_for_html(self):
        find_word = session.get('find_word')
        client_word = session.get('client_word')
        if client_word:
            all_data = self.game.word_finder(client_word=client_word, find_word=find_word, user=self.user)
            return list(all_data) + [find_word, client_word]
        return False


    def main(self):
        #self.set_user_db()
        self.load_data()
        self.post_request()

        all_data = self.data_for_html()
        return all_data
        