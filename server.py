from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db
from model import User, House, HouseChore, Chore, UserChore
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

@app.route("/twilio", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""
 
    from_number = request.values.get('From', None)
    if from_number in callers:
        message = callers[from_number] + ", thanks for the message!"
        client.messages.create(
			to=from_number, 
			from_=MY_TWILIO_NUMBER, 
			body=message,  
        )
    else:
        message = "Monkey, thanks for the message!"
 
    resp = twilio.twiml.Response()
    resp.message(message)
 
    return str(resp)

@app.route("/", methods=['GET'])
def login():
    """Index route will be a login page requesting username and password"""

    return render_template('index.html')

@app.route("/register", methods=['GET'])
def register():
    """Request user and house information from the admin user."""

    return render_template('register.html')

@app.route("/invited_register/<int:user_id>", methods=['GET'])
def invited_register(user_id):
    """Request user information from invited (non-admin) users."""

    invited_user = User.query.filter_by(id=user_id).one()

    return render_template('invited_register.html', invited_user=invited_user)


@app.route("/add_admin_user", methods=['POST', 'GET'])
def add_admin_user():
    """Add admin user into database from registration form."""

    # get new user information
    username = request.form.get('username')
    phone = request.form.get('phone')
    password = request.form.get('password')

    # get new house information
    house_name = request.form.get('house_name')

    new_user = User(username=username,
                    phone=phone,
                    password=password,
                    is_admin=True)

    db.session.add(new_user)
    db.session.commit()


    return redirect('/create_house_pref')

@app.route("/create_house_pref", methods=['GET'])
def create_house_pref():
    """Scheduling preference where admin user picks chores, invites house members and schedule length."""

    chore_objs = Chore.query.all()

    return render_template('create_house_pref.html', chore_objs=chore_objs)

@app.route("/create_house_pref_2", methods=['GET'])
def create_house_pref_2():
    """Step 2 of 3 for creating house preferences. Step 2 is rendering a modal window of each
    chore chosen in Step 1 in order to set the week frequency and day of week due."""

    return render_template('create_house_pref_2.html')

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

@app.route("/house_pref_view", methods=['GET'])
def house_pref_view():
    """Renders summary of house preferences."""

    return render_template('house_pref_view_only.html')
print "you are awesome"
 
if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(debug=True)