# For writing application routes , import application
from app import application
from flask import  render_template , request , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# For refering to the database import the database object db and the models module
from app import models,db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash

# user_loader callback
@login_manager.user_loader
def user_loader(id):
    return models.UserCredentials.query.get(id)

@application.route("/")
def home():
    return "CyberHawk"


# Route to register new player
@application.route("/addPlayer", methods = ["POST"])
def addPlayer():
    data = request.get_json()

    # Check if email and username entered are unique
    if models.UserCredentials.query.filter_by(userEmail = data['userEmail']).first() != None:
        response = {
            "success": False,
            "data": "Email already registered, try logging in"
        }

    elif models.UserCredentials.query.filter_by(userName = data['userName']).first() != None:
        response = {
            "success": False,
            "data": "Username is taken, try another Username"
        }

    # Register player
    else:
        playerCredentials = models.UserCredentials(data["userEmail"], data["userName"], data["userPassword"])
        db.session.add(playerCredentials)
        db.session.commit()

        # Add player details to models.UserDetails db
        playerDetails = models.UserDetails(playerCredentials.id, playerCredentials.userName, data["userPhone"], data["userCollege"], 1, 0)
        db.session.add(playerDetails)
        db.session.commit()

        response = {
            "success": True,
            "data": "NULL"
        }

    return jsonify(response)


# Route to modify player
@application.route("/modifyPlayer", methods = ["POST"])
@login_required
def modifyPlayer():
    data = request.get_json()

    # Check if email and username entered are unique
    if db.session.query(models.UserCredentials.userEmail).filter(models.UserCredentials.userEmail == data["userEmail"]).count() > 0:
        response = {
            "success": False,
            "data": "Could not modify, email already registered"
        }

    elif db.session.query(models.UserCredentials.userName).filter(models.UserCredentials.userName == data["userName"]).count() > 0:
        response = {
            "success": False,
            "data": "Could not modify, username is taken, try another username"
        }

    # Modify player
    else:
        # Get the current logged in player from DBs
        playerid = current_user.get_id()
        playerCredentials = models.UserCredentials.query.get(playerid)
        playerDetails = models.UserDetails.query.get(playerid)

        # Modify player records
        playerCredentials.userName = data["userName"]
        playerCredentials.userEmail = data["userEmail"]
        playerDetails.userName = data["userName"]
        playerDetails.userPhone = data["userPhone"]
        playerDetails.userCollege = data["userCollege"]
        db.session.commit()
        response = {
            "success": True,
            "data": "NULL"
        }

    return jsonify(response)


# Admin Route to get player
@application.route("/admin/getPlayer", methods = ["POST"])
@login_required
def getPlayer():
    # Get the current logged in player from DBs
    playerid = current_user.get_id()
    playerCredentials = models.UserCredentials.query.get(playerid)
    if playerCredentials.userName != "admin":
        response = {
            "success": False,
            "data": "Only accesible by admin"
        }
    else:
        data = request.get_json()
        playerCredentials = models.UserCredentials.query.get(data["id"])
        playerDetails = models.UserDetails.query.get(data["id"])
        response = {
            "success": True,
            "data": {
                "userID": playerDetails.id,
                "userName": playerDetails.userName,
                "userEmail": playerCredentials.userEmail,
                "level": playerDetails.userLevel,
            }
        }

    return jsonify(response)


# Route to login
@application.route("/login", methods = ["POST"])
def login():
    data = request.get_json()

    # Verify username and password
    if db.session.query(models.UserCredentials.userName).filter(models.UserCredentials.userName == data["userName"]).count() > 0:
        player = db.session.query(models.UserCredentials).filter(models.UserCredentials.userName == data["userName"]).first()
        if check_password_hash(player.userPassword, data["userPassword"]):
            login_user(player, remember=True)
            response = {
                "success": True,
                "data": {
                    "id": player.id
                }
            }

        else:
            response = {
                "success": False,
                "error": "incorrect password"
            }

    else:
        response = {
            "success": False,
            "error": "invalid username"
        }

    return jsonify(response)


# Route to logout
@application.route("/logout")
@login_required
def logout():
    logout_user()
    response = {
        "success": True,
        "data": "NULL"
    }
    return jsonify(response)


# Route to reset password
@application.route("/resetPassword", methods = ["POST"])
def resetPassword():
    data = request.get_json()
    if db.session.query(models.UserCredentials.userEmail).filter(models.UserCredentials.userEmail == data["userEmail"]).count() > 0:
        playerCredentials = models.UserCredentials.query.filter_by(userEmail = data["userEmail"]).first()
        generatedPW = generate_password_hash("cyberhawk")
        playerCredentials.userPassword = generatedPW
        db.session.commit()
        response = {
            "success": True,
            "data": "NULL"
        }
    else:
        response = {
            "success": False,
            "data": "Email address not registered"
        }

    return jsonify(response)


########################### QUESTION MANAGEMENT ROUTES ################################
## Temporary method to add new questions
## Incorporate into admin app somehow
@application.route("/addquestion" , methods=['GET' , 'POST'])
@login_required
def add_new_question():
	if request.method == 'GET':
		return "Post raw json with keys question , answer ,hint1 , hint2 , hint3"
	else:
		recieved_question =request.get_json()
        curr_user = current_user.get_id()
        if curr_user != 1:
            return "No Access"
        count_players = 0
        new_question = models.Questions_Answers(recieved_question['question'] , recieved_question['answer'] , recieved_question['hint1'] , recieved_question['hint2'] , recieved_question['hint3'] , count_players)
        db.session.add(new_question)
        db.session.commit()
        return "New Question added. Question id is "

##Get Question App route
## Takes user id as input , queries database for current level and queries the questins database for the question
@application.route("/getquestion" , methods = ['GET' , 'POST'])
@login_required
def getquestion():
	if request.method == 'GET':
		return "Post User ID"
	else:
		recieved_user_id = request.get_json()
		user_data = models.UserDetails.query.filter_by(id = recieved_user_id['userid']).first()
		ques_toret = models.Questions_Answers.query.filter_by(question_num = user_data['userLevel']).first()
        if ques_toret == None:
            return "fuck"

        json_toret = { "success" : True , "data" : {"question_id" : user_data['userLevel'] , "question" : ques_toret['question']} }
        return jsonify(json_toret)

## Check if answer is correct
## Takes question id  , user's id and user's answer as input . Queries database for question ,
## checks if answer is corect . IF answer is correct , increments level field in USer database
@application.route("/checkanswer" , methods = ['GET' , 'POST'])
@login_required
def check():
	rec_data = request.get_json()
	question_tocheck = models.Questions_Answers.query.filter_by(question_num = rec_data['questionid']).first()
	if rec_data['answer'] == question_tocheck['answer']:
		json_toret = { 'success' : True , "data": "NULL" }
		user_data = models.UserDetails.query.filter_by(id = rec_data['userid']).first()
		user_data.userLevel += 1
		user_data.userHints = 0
		db.session.commit()
	else:
		json_toret = { 'success' : False , "data": "NULL" }
	return jsonify(json_toret)

@application.route("/gethint" , methods = ['GET' , 'POST'])
@login_required
def gethints():
	rec_data = request.get_json()
	question = models.Questions_Answers.query.filter_by(question_num = rec_data['questionid']).first()
	user_data = models.UserDetails.query.filter_by(id = rec_data['userid']).first()
	json_toret = {"success" : True }
	if user_data['userHints'] == 0:
		json_toret['data'] = { "hints" : [{'hintid' : 1 , "hint" : question['hint1']}]}
	elif user_data['userHints'] == 1:
		json_toret['data'] = { "hints" : [{'hintid' : 1 , "hint" : question['hint1']} , {"hintid" : 2 , "hint" : question['hint2']} ]}
	else:
		json_toret['data'] = { "hints" : [{'hintid' : 1 , "hint" : question['hint1']} , {"hintid" : 2 , "hint" : question['hint2']} , {'hintid' : 3 , "hint" : question['hint3']} ]}
	user_data.userHints = user_data.userHints + 1
	db.session.commit()
	return jsonify(json_toret)
