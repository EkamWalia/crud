
from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import os
#User login Database
class UserCredentials(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userEmail = db.Column(db.String(120), unique=True, nullable=False)
    userName = db.Column(db.String(64), unique=True)
    userPassword = db.Column(db.String(120), nullable=False)

    def __init__(self, userEmail, userName, userPassword):
        self.userEmail = userEmail
        self.userName = userName
        self.userPassword =  generate_password_hash(userPassword)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __getitem__(self,item):
        return getattr(self,item)

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(64))
    userPhone = db.Column(db.String(20))
    userCollege = db.Column(db.String(120))
    userLevel = db.Column(db.Integer)
    userHints = db.Column(db.Integer)

    def __init__(self, id, userName, userPhone, userCollege, userLevel, userHints):
        self.id = id
        self.userName = userName
        self.userPhone = userPhone
        self.userCollege = userCollege
        self.userLevel = userLevel
        self.userHints = userHints

    def __getitem__(self,item):
        return getattr(self,item)

## Database containing all questions , respective answers, and hints
## Accessed by admin to add new Questions and by users to get the next question
class Questions_Answers(db.Model):
    question_num = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String(100))
    answer = db.Column(db.String(50))
    hint1 = db.Column(db.String(50))
    hint2 = db.Column(db.String(50))
    hint3 = db.Column(db.String(50))
    players = db.Column(db.Integer)

    def __init__(self , question , answer , hint1 , hint2 , hint3 , players):
        self.question = question
        self.answer= answer
        self.hint1 = hint1
        self.hint2 = hint2
        self.hint3 = hint3
        self.players = players

    def __getitem__(self,item):
        return getattr(self,item)

db.create_all()
db.session.commit()
