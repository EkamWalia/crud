from app import db

#User login Database
class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(50))
    emailid = db.Column(db.String(60))
    password = db.Column(db.String(30))
    college = db.Column(db.String(60))

    def __init__(self , name , emailid , password , college):
        self.name = name
        self.emailid = emailid
        self.password = password
        self.college = college

db.create_all()
db.session.commit()
