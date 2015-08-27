import datetime
from flask import Flask, request, redirect, session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import TwilioRestClient 
import twilio.twiml
from server import client, app, MY_TWILIO_NUMBER, MY_PHONE_NUMBER
from model import connect_to_db, db
from model import User, House, HouseChore, Chore, UserChore

############################################################################## 

def get_chores(usr):
	return UserChore.query.filter(UserChore.user_id==usr.id).all()

def day_of_alerts(today=datetime.datetime.now()):
	yesterday = today - datetime.timedelta(days=1)
	tomorrow = today + datetime.timedelta(days=1)

	# get the users that have chores due today
	users_userchores =  db.session.query(User, UserChore).join(UserChore).filter(UserChore.due_date > yesterday, UserChore.due_date < tomorrow, UserChore.is_active==True).all()

	# create a dictionary {user: [userchores list]} 
	alert_dict = {}
	# import pdb; pdb.set_trace()
	for user, userchore in users_userchores:
		if user in alert_dict:
			alert_dict[user].append(userchore)
		else:
			alert_dict[user] = [userchore]

	# create a list of userchores if there are multiple to text out
	text_chore_list = []

	for user in alert_dict:	
		if len(alert_dict[user]) == 1:
			userchore_name = alert_dict[user][0].chore.name
			message = "Choreme: " + userchore_name + " is due today :)."
			client.messages.create(
				# to=userchore.user.phone,
				to=MY_PHONE_NUMBER,
				from_=MY_TWILIO_NUMBER,
				body=message)
			resp = twilio.twiml.Response()
			resp.message(message)
		elif len(alert_dict[user]) > 1:
			for index, userchore in enumerate(alert_dict[user]):
				if index == 0:
					message = str(index+1) + " " + userchore.chore.name + "\n"
				else:
					message = message + str(index+1) + " " + userchore.chore.name + "\n"
			# get rid of unicode
			message = message.encode('ascii','ignore')

			client.messages.create(
				# to=userchore.user.phone,
				to=MY_PHONE_NUMBER,
				from_=MY_TWILIO_NUMBER,
				body="Choreme: you have the following chores due :)\n" + message.rstrip())
			resp = twilio.twiml.Response()
			resp.message(message)





############################################################################## 

if __name__ == "__main__":
	connect_to_db(app)
	day_of_alerts()
	print "Connected to DB."

