from flask_login import UserMixin
from datetime import datetime

from applications import db
from .utilities.skill_lvl_wrdle import set_skill_lvl


class UserInfo(db.Model, UserMixin):
    __tablename__ = 'user_info'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    data_time = db.Column(db.DateTime, default=datetime.now())
    
    wordle_5_let = db.relationship('Wordle5Letters', backref='wordle_5', uselist=False)
    wordle_6_let = db.relationship('Wordle6Letters', backref='wordle_6', uselist=False)
    wordle_7_let = db.relationship('Wordle7Letters', backref='wordle_7', uselist=False)
    reviews = db.relationship('Reviews', backref="poster")
    wd_statistics = db.relationship('WordleStatistics', backref="stats", uselist=False)

    def get_id(self):
        return str(self.user_id)

    # @property
    # def password(self):
    #     raise AttributeError('password is not readable')
    
    # @password.setter
    # def password(self, psw_cl):
    #     self.password = generate_password_hash(psw_cl)

    # def verify_password(self, psw_cl):
    #     return check_password_hash(self.password, psw_cl)

    def __repr__(self):
        return '<Name %r>' % self.name
    

class Reviews(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'))
    review = db.Column(db.String(150), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Name %r>' % self.name


class WordleStatistics(db.Model):
    __tablename__ = 'wordle_statistics'
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'), primary_key=True)
    total_guessed = db.Column(db.Integer, default=0)
    total_attempt = db.Column(db.Integer, default=0)
    first_try = db.Column(db.Integer, default=0)
    third_try = db.Column(db.Integer, default=0)
    average_attempt = db.Column(db.Integer, default=0)
    max_attempt = db.Column(db.Integer, default=0)
    wd_len_5 = db.Column(db.Integer, default=0)
    wd_len_6 = db.Column(db.Integer, default=0)
    wd_len_7 = db.Column(db.Integer, default=0)
    wd_skill_lvl = db.Column(db.String(20), default='human')
    last_update = db.Column(db.DateTime, default=datetime.now())



    def update_user_stats(self, client_word, find_word, attempt_number, wd_len):
        if client_word == find_word:
            attempts = attempt_number
            self.total_guessed += 1

            if attempts == 1:
                self.first_try += 1
            elif attempts <= 3:
                self.third_try += 1
            
            if attempts > self.max_attempt:
                self.max_attempt = attempts

            if wd_len == 5:
                self.wd_len_5 += 1
                print(f'5 +1')
            elif wd_len == 7:
                self.wd_len_7 += 1
                print(f'7 +1')
            elif wd_len == 6:
                self.wd_len_6 += 1
                print(f'6 +1')

            print(f'WD LEN {wd_len}')

        self.total_attempt += 1
        if self.total_guessed != 0:
            self.average_attempt = self.total_attempt / self.total_guessed
        self.wd_skill_lvl = set_skill_lvl(int(self.average_attempt))
        self.last_update = datetime.now()
        db.session.commit()
        return True


    def __repr__(self):
        return '<Name %r>' % self.name


class Wordle5Letters(db.Model):
    __tablename__ = 'wordle_5_letters'
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'), primary_key=True)
    client_word = db.Column(db.String(20), nullable=True)
    find_word = db.Column(db.String(20),  nullable=True)
    attempts = db.Column(db.Integer, default = 0)
    word_list = db.Column(db.String(150), nullable=True)
    global_direct = db.Column(db.String(30),nullable=True)
    global_indirect = db.Column(db.String(30), nullable=True)
    indirect_match = db.Column(db.String(30), nullable=True)
    direct_match = db.Column(db.String(30), nullable=True)
    last_win = db.Column(db.Boolean, default=True)


    def update_wordle(self, client_word, find_word, global_direct, global_indirect, word_history, attempt_number, indirect_match, direct_match, last_win):
        self.client_word = client_word
        self.find_word = find_word
        self.global_direct = global_direct
        self.global_indirect = global_indirect
        self.word_list = word_history
        self.attempts = attempt_number
        self.indirect_match = indirect_match
        self.direct_match = direct_match
        self.last_win = last_win

        db.session.commit()
        return True


class Wordle6Letters(db.Model):
    __tablename__ = 'wordle_6_letters'
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'), primary_key=True)
    client_word = db.Column(db.String(20), nullable=True)
    find_word = db.Column(db.String(20),  nullable=True)
    attempts = db.Column(db.Integer, default = 0)
    word_list = db.Column(db.String(150), nullable=True)
    global_direct = db.Column(db.String(30),nullable=True)
    global_indirect = db.Column(db.String(30), nullable=True)
    indirect_match = db.Column(db.String(30), nullable=True)
    direct_match = db.Column(db.String(30), nullable=True)
    last_win = db.Column(db.Boolean, default=True)



    def update_wordle(self, client_word, find_word, global_direct, global_indirect, word_history, attempt_number, indirect_match, direct_match, last_win):
        self.client_word = client_word
        self.find_word = find_word
        self.global_direct = global_direct
        self.global_indirect = global_indirect
        self.word_list = word_history
        self.attempts = attempt_number
        self.indirect_match = indirect_match
        self.direct_match = direct_match
        self.last_win = last_win

        db.session.commit()
        return True
    

class Wordle7Letters(db.Model):
    __tablename__ = 'wordle_7_letters'
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'), primary_key=True)
    client_word = db.Column(db.String(20), nullable=True)
    find_word = db.Column(db.String(20),  nullable=True)
    attempts = db.Column(db.Integer, default = 0)
    word_list = db.Column(db.String(150), nullable=True)
    global_direct = db.Column(db.String(30),nullable=True)
    global_indirect = db.Column(db.String(30), nullable=True)
    indirect_match = db.Column(db.String(30), nullable=True)
    direct_match = db.Column(db.String(30), nullable=True)
    last_win = db.Column(db.Boolean, default=True)


    def update_wordle(self, client_word, find_word, global_direct, global_indirect, word_history, attempt_number, indirect_match, direct_match, last_win):
        self.client_word = client_word
        self.find_word = find_word
        self.global_direct = global_direct
        self.global_indirect = global_indirect
        self.word_list = word_history
        self.attempts = attempt_number
        self.indirect_match = indirect_match
        self.direct_match = direct_match
        self.last_win = last_win

        db.session.commit()
        return True