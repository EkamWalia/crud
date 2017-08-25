# For writing application routes , import application
from app import application

from flask import  render_template , request
from flask_sqlalchemy import SQLAlchemy
# For refering to the database import the database object db and the models module
from app import models,db

#
@application.route("/")
def index():
	return "Working....."

@application.route("/register" , methods=['GET' , 'POST'])
def register_newuser():
	if request.method == 'GET':
		return "POST a raw JSON with keys name , password , emailid , college"
	else:
		recieved_data = request.get_json()
		#User class is in the models module hence use models.User
		new_user_data = models.User(recieved_data['name'] , recieved_data['emailid'] , recieved_data['password'] , recieved_data['college'])
		db.session.add(new_user_data)
		db.session.commit()
		return "Succesfully registered"
