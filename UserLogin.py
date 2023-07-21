from main import db

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Varchar(db.Varchar(20))
    email = db.Column(db.Varchar(50), unique=True)
    password = db.Column(db.Varchar(100))

    