from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class UserInfo(db.Model, UserMixin):
    __tablename__ = 'user_info'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    data_time = db.Column(db.DateTime, default=datetime.now())
    
    reviews = db.relationship('Reviews', backref="poster")
    statistics = db.relationship('Statistics', backref="stats", uselist=False)

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
    review = db.Column(db.String(15), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Name %r>' % self.name
    

class Statistics(db.Model):
    __tablename__ = 'statistics'
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'), primary_key=True)
    total_guessed = db.Column(db.Integer, default=0)
    total_attempt = db.Column(db.Integer, default=0)
    first_try = db.Column(db.Integer, default=0)
    third_try = db.Column(db.Integer, default=0)
    average_attempt = db.Column(db.Integer, default=0)
    max_attempt = db.Column(db.Integer, default=0)
    last_update = db.Column(db.DateTime, default=datetime.now())


    def update_user_stats(self, client_word, find_word, attempt_number):
        if client_word == find_word:
            attempts = attempt_number
            self.total_guessed += 1
            if attempts == 1:
                self.first_try += 1
            elif attempts <= 3:
                self.third_try += 1
            elif attempts > self.max_attempt:
                self.max_attempt = attempts

        self.total_attempt += 1
        self.average_attempt = self.total_attempt / self.total_guessed
        self.last_update = datetime.now()
        db.session.commit()
        return True


    def __repr__(self):
        return '<Name %r>' % self.name
    