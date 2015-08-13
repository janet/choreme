from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm.exc import NoResultFound
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
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN'] 
 
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) 

MY_PHONE_NUMBER = os.environ['MY_PHONE_NUMBER']
 
# adding specific numbers for personalized response
callers = {
   MY_PHONE_NUMBER : "you are the best programmer", 
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
    
    try:
        session["user_id"]
        return redirect("/calendar_view")
    except KeyError:
        session["user_id"] = None
        return render_template("login.html")

@app.route("/register", methods=['GET'])
def register():
    """Request user registration details from the admin user."""

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

    session['user_id'] = new_user.id
    flash("session user_id: ", session['user_id'])


    return redirect('/create_house_pref')

@app.route("/create_house_pref", methods=['POST','GET'])
def create_house_pref():
    """Scheduling preference where admin user picks chores, invites house members and schedule length."""

    chore_objs = Chore.query.all()

    return render_template('create_house_pref.html', chore_objs=chore_objs)

@app.route("/pass_chore_freq", methods=['POST'])
def temp_save_chore_freq():
    """Pass chore frequency from modal window form to create_house_pref on modal window
    save."""
    
    chore_name = request.form.get('chore')
    week_freq = request.form.get('week_freq')
    day = request.form.get('day')

    return jsonify({'chore_name': chore_name,
                    'week_freq': week_freq,
                    'day': day})

@app.route("/scheduling_algorithm", methods=['POST'])
def scheduling_algorithm():
    """This route assigns chores to users based on the house preferences inputted and 
    redirects to calendar_view"""

    house_name = request.form.get('house_name')
    admin_phone = request.form.get('admin_phone')
    housemate_count = int(request.form.get('housemate_count'))
    num_weeks = request.form.get('num_weeks')

    # add new user with phone number
    for i in range(housemate_count):
        housemate_input_name = "housemate_phone" + str(i+1)
        print housemate_input_name
        try:
            request.form.get(housemate_input_name)
            housemate_phone = request.form.get(housemate_input_name)
            if housemate_phone is not None:
                new_user = User(phone=housemate_phone)
                db.session.add(new_user)
                db.session.commit()
        except:
            pass

    #create new 


    # print "house_name: %s, admin_phone: %s, hm_phone_list: %s" % (house_name, admin_phone, hm_phone_list)

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

@app.route('/process_login', methods=['POST'])
def process_login():
    """Process login form: Authenticate user password and error if incorrect."""

    username = request.form.get("username")
    password = request.form.get("password")
    
    try:
        user = User.query.filter_by(username=username).one()
        if user.password != password:
            flash("Password not recognized. Please re-enter.")
            return redirect('/') #re-enter password
        else:
            # adding logged in user to session if u/n & p/w match database
            session['user_id'] = user.id
            # also add logged in user's house_id to allow easy save of chore freq in house pref
            session['house_id'] = user.house.id
            flash("Logged in")
            flash("user_id: %s house_id: %s" % (session['user_id'], session['house_id']))
            return redirect('/personal_view')


    except NoResultFound:
        flash("Username not recognized. Please re-enter or register below.")
        return redirect('/')

@app.route('/logout')
def logout():
    """Logout route that redirects to the homepage"""
    flash("Logged out")

    session['user_id'] = None

    return redirect('/')
   

print "you are awesome"
 
if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(debug=True)