from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db
from twilio.rest import TwilioRestClient 
import twilio.twiml
import os

############################################################################## 
# Flask 
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

############################################################################## 
 
# Twilio
ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN'] 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

my_phone_number = os.environ['MY_PHONE_NUMBER']
 
# adding specific numbers for personalized response
callers = {
   my_phone_number : "you are the best programmer", 
}

# my twilio phone number
MY_TWILIO_NUMBER = os.environ['MY_TWILIO_NUMBER']

##############################################################################

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""
 
   #  from_number = request.values.get('From', None)
   #  if from_number in callers:
   #      message = callers[from_number] + ", thanks for the message!"
   #      client.messages.create(
			# to=from_number, 
			# from_=MY_TWILIO_NUMBER, 
			# body=message,  
   #      )
   #  else:
   #      message = "Monkey, thanks for the message!"
 
   #  resp = twilio.twiml.Response()
   #  resp.message(message)
 
   #  return str(resp)

    return render_template('base.html')

@app.route("/sign_up", methods=['GET'])
def sign_up():
    """Request user information for both invited and new users and add to the database"""

    return render_template('sign_up.html')

@app.route("/create_house", methods=['GET'])
def create_house():
    """Request information to create a new house."""

    return render_template('create_house.html')

@app.route("/invite_housemates", methods=['GET'])
def invite_housemates():
    """Request other housemate emails and send emails to invite them to house."""

    return render_template('invite_housemates.html')

@app.route("/create_house_pref_1", methods=['GET'])
def create_house_pref_1():
    """Step 1 of 3 for creating house preferences. Step 1 is selecting chores for the household."""

    return render_template('create_house_pref_1.html')

@app.route("/create_house_pref_2", methods=['GET'])
def create_house_pref_2():
    """Step 2 of 3 for creating house preferences. Step 2 is rendering a modal window of each
    chore chosen in Step 1 in order to set the week frequency and day of week due."""

    return render_template('create_house_pref_2.html')

@app.route("/create_house_pref_3", methods=['GET'])
def create_house_pref_3():
    """Step 3 of 3 for creating house preferences. Step 3 is a confirmation page of the 
    house chore options and requests the schedule end date."""

    return render_template('create_house_pref_3.html')

@app.route("/scheduling_algorithm", methods=['GET'])
def scheduling_algorithm():
    """This route assigns chores to users based on the house preferences inputted and 
    redirects to calendar_view"""

    return redirect('/calendar_view')

@app.route("/calendar_view", methods=['GET'])
def calendar_view():
    """Renders the calendar view of the user's house and chores assigned."""

    return render_template('calendar_view.html')

@app.route("/personal_view", methods=['GET'])
def personal_view():
    """Renders the personal task list view of the user's assigned chores."""

    return render_template('personal_view.html')

print "you are awesome"
 
if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(debug=True)