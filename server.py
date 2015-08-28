import datetime
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
   MY_PHONE_NUMBER : "me", 
}

# my twilio phone number
MY_TWILIO_NUMBER = os.environ['MY_TWILIO_NUMBER']

##############################################################################



@app.route("/", methods=['GET'])
def login():
    """Index route will be a login page requesting username and password"""

    try:
        if session["user_id"] is None:
            return render_template("login.html")
        return redirect("/calendar_view")
    except KeyError:
        session["user_id"] = None
        return render_template("login.html")


@app.route("/register", methods=['GET'])
def register():
    """Request user registration details from the admin user."""

    return render_template('register.html')


@app.route("/<int:user_id>", methods=['GET']) # this is a short url in order to fit sms size limits
def invited_register(user_id):
    """Request user information from invited (non-admin) users."""

    invited_user = User.query.filter_by(id=user_id).one()

    return render_template('invited_register.html', invited_user=invited_user)


@app.route("/add_admin_user", methods=['POST'])
def add_admin_user():
    """Add admin user into database from registration form."""

    # get new user information
    username = request.form.get('username')
    phone = request.form.get('phone')
    password = request.form.get('password')

    new_user = User(username=username,
                    phone=phone,
                    password=password,
                    is_admin=True)

    db.session.add(new_user)
    db.session.commit()

    admin_user_id = User.query.filter(User.username==username).one().id
    print admin_user_id

    session['user_id'] = admin_user_id
    print session['user_id']
    # flash("session user_id: " + str(session['user_id']))

    return redirect('/create_house_pref')

@app.route("/add_invited_user", methods=['POST'])
def add_invited_user():
    """Update invited user in database with username and password info.
    Redirect to the calendar_view."""

    # get username, password and id info
    username = request.form.get('username')
    password = request.form.get('password')
    user_id = request.form.get('user_id')

    # update user in database
    user = User.query.get(user_id)
    user.username = username
    user.password = password

    # commit changes to the database
    db.session.commit()

    # add user_id & house_id to the session
    session["user_id"] = user_id
    session["house_id"] = user.house.id

    return redirect('/calendar_view')

@app.route("/process_texts", methods=['POST', 'GET'])
def process_texts():
    """Process text replies and update database with chore done."""

    print "you got here"

    from_number = request.form.get('From')
    from_body = request.form.get('Body')

    if from_body == "DONE":
        User.query.filter(User.phone==from_number, User.userchore.due_date>yesterday, User.userchore).one()

    print from_body



    return redirect("/")

@app.route("/create_house_pref", methods=['POST','GET'])
def create_house_pref():
    """Scheduling preference where admin user picks chores, 
    invites house members and schedule length.
    Also processes re-scheduling."""

    # get the chore objects to render in the select chores table
    chore_objs = Chore.query.all()

    # get the admin phone that was just added
    admin_phone = User.query.get(session['user_id']).phone


    # if there is already a schedule, render it
    try:
        session["house_id"]
        # get the current chore information to display for reference purposes
        house_name = House.query.get(session["house_id"]).name
        # over-write the admin phone from before in case a non-admin is viewing
        admin_phone = User.query.filter(User.house_id==session['house_id'], User.is_admin==1).one().phone

        # unpack this in jinja to get the housemate phones
        housemates_list = User.query.filter(User.house_id==session['house_id'], User.is_admin==0).all()

        # get house_chores
        housechores_list = HouseChore.query.filter(HouseChore.house_id==session['house_id']).all()

        # get current schedule start date and length
        house_start_date = House.query.get(session["house_id"]).start_date
        house_num_weeks = House.query.get(session["house_id"]).num_weeks

        return render_template('create_house_pref.html', chore_objs=chore_objs,
                                                         house_name=house_name,
                                                         admin_phone=admin_phone,
                                                         housemates_list=housemates_list,
                                                         housechores_list=housechores_list,
                                                         house_start_date=datetime.datetime.strftime(house_start_date, "%m/%d/%y"),
                                                         house_num_weeks=house_num_weeks
                                                         )

    # if there is no house_id in the session, this is the first time the page is
    # visited, so render the template with no previous schedule info
    except KeyError:
        pass
    except TypeError:
        pass

    return render_template('create_house_pref.html', chore_objs=chore_objs,
                                                     admin_phone=admin_phone)


@app.route("/pass_chore_freq", methods=['POST'])
def pass_chore_freq():
    """Pass chore frequency from modal window form to create_house_pref on modal window
    save."""
    
    chore_name = request.form.get('chore')
    week_freq = request.form.get('week_freq')
    day = request.form.get('day')

    return jsonify({'chore_name': chore_name,
                    'week_freq': week_freq,
                    'day': day})


@app.route("/create_user_chores", methods=['POST'])
def create_user_chores():
    """This route assigns chores to users based on the house preferences inputted and 
    redirects to calendar_view"""

    house_name = request.form.get('house_name')
    housemate_count = int(request.form.get('housemate_count'))
    housechore_count = int(request.form.get('hidden_count_of_chores'))
    num_weeks = int(request.form.get('num_weeks'))


    # create new house with house name
    new_house = House(name=house_name, num_weeks=num_weeks)
    db.session.add(new_house)
    db.session.commit()

    # add the house id to the session
    house = House.query.filter(House.name==house_name).one()
    house_id = house.id
    session['house_id'] = house_id

    # add house id to the admin user
    admin_user = User.query.get(session['user_id'])
    admin_user.house_id = house_id

    # create new user with phone number
    for i in range(housemate_count):
        housemate_phone = "housemate_phone" + str(i+1)
        try:
            request.form.get(housemate_phone)
            housemate_phone = request.form.get(housemate_phone)
            if housemate_phone is not None:
                new_user = User(phone=housemate_phone,
                                house_id=house_id)
                db.session.add(new_user)
        except:
            pass

    # create new house chore
    for i in range(housechore_count):
        housechore_input_name = "chores" + str(i+1)
        try:
            request.form.get(housechore_input_name)
            housechore_input = request.form.get(housechore_input_name)
            if housechore_input is not None:
                chore, week_freq, day = housechore_input.split('|')
                chore_id = Chore.query.filter(Chore.name==chore).one().id
                new_housechore = HouseChore(house_id=house_id,
                                            chore_id=chore_id,
                                            day=day,
                                            week_freq=int(week_freq)
                                            )
                db.session.add(new_housechore)
        except:
            pass

    # commit new housemates and house chores here
    db.session.commit()

    # create new user chores

    # get the date from the house and determine the actual start date
    init_sched_date = house.start_date

    # create a list of housemates and count the number to assign out to them
    housemates_list = House.query.get(house_id).users
    num_housemates = len(housemates_list)

    # use enumerate to create an index for each house chore that allows for easy assignment
    for index, house_chore in enumerate(house.house_chores):
        print "index: %s, house_chore: %s" % (index, house_chore)

        # while schedule start day (ie Sunday) != house chore day
        while datetime.datetime.strftime(init_sched_date,"%A") != house_chore.day: 
            init_sched_date += datetime.timedelta(days=1)

        # this is the first occurence of the chore
        first_sched_date = init_sched_date
        print "first_sched_date = ", first_sched_date

        print "int(house.num_weeks)", int(house.num_weeks)
        print "int(house_chore.week_freq)", int(house_chore.week_freq)

        # create user chores for each occurrence
        for i in range(house.num_weeks / house_chore.week_freq):
            due_date = first_sched_date + datetime.timedelta(days=((i)*(house_chore.week_freq*7)))

            housemate = housemates_list[(index + i) % num_housemates]
            print "HOUSEMATE: ", housemate

            print "user_id: %s, chore_id: %s, due_date: %s" % (housemate.id, house_chore.chore.id, due_date.strftime("%A, %m/%d/%y"))

            new_userchore = UserChore(user_id=housemate.id, 
                                        chore_id=house_chore.chore.id,
                                        due_date=due_date)

            db.session.add(new_userchore)
    db.session.commit()

    # return redirect("/calendar_view") # use this to conserve texts for testing
    return redirect("/invite_housemates") 

@app.route("/recreate_user_chores", methods=['POST'])
def recreate_user_chores():
    """Routed from create_house_pref view to reschedule chores. This route is called
    to create user chores after the first time chores are created and diffs against
    against previously entered house prefs."""

    housemate_count = int(request.form.get('housemate_count'))
    housechore_count = int(request.form.get('hidden_count_of_chores'))
    num_weeks = int(request.form.get('num_weeks'))


    # get the house_id from the session
    house_id = session['house_id']
    house = House.query.get(house_id)

    # get the admin phone
    admin_phone = User.query.filter(User.house_id==session['house_id'], User.is_admin==1).one().phone

    # get the current housemates and diff against entered
    housemates_phone_set = set([admin_phone]) # previously entered + admin
    new_housemates_set = set([admin_phone]) # newly entered and in previously entered + admin
    for housemate in House.query.get(house_id).users:
        housemates_phone_set.add(housemate.phone)

    # add new housemate if new 
    for i in range(housemate_count):
        housemate_phone = "housemate_phone" + str(i+1)
        try:
            request.form.get(housemate_phone)
            housemate_phone = request.form.get(housemate_phone)
            if housemate_phone is None:
                pass
            elif str(housemate_phone) not in housemates_phone_set:
                # new user in the house
                new_user = User(phone=str(housemate_phone),
                                house_id=house_id)
                db.session.add(new_user)
            elif str(housemate_phone) in housemates_phone_set:
                new_housemates_set.add(str(housemate_phone))
        except:
            pass

    # remove housemate if no longer in house
    remove_housemate = housemates_phone_set - new_housemates_set
    if remove_housemate:
        for housemate_phone in remove_housemate:
            remove_user = User.query.filter(User.phone==housemate_phone, User.house_id==house_id).one()
            remove_user.house_id = None # unassociate user from house

    # remove any user_chores that were previously created for a future date
    inactivate_userchores = UserChore.query.filter(UserChore.due_date>=datetime.datetime.now()).all()
    for userchore in inactivate_userchores:
        userchore.is_active = False # deactivate userchore

    # remove housechore from house
    for housechore in house.house_chores:
        housechore.house_id = None # deactivate previous housechores_list

    # update House start_date
    House.query.get(house_id).start_date = datetime.datetime.now()


    # commit changes: adding/removing housemates based on new inputs
    # deactivating user_chores that were previously created for a future date
    # deactivate old housechores and updating start date
    db.session.commit()

    # create new house chore
    for i in range(housechore_count):
        housechore_input_name = "chores" + str(i+1)
        try:
            request.form.get(housechore_input_name)
            housechore_input = request.form.get(housechore_input_name)
            if housechore_input is not None:
                chore, week_freq, day = housechore_input.split('|')
                chore_id = Chore.query.filter(Chore.name==chore).one().id
                new_housechore = HouseChore(house_id=house_id,
                                            chore_id=chore_id,
                                            day=day,
                                            week_freq=int(week_freq)
                                            )
                db.session.add(new_housechore)
        except:
            pass

    # commit new house chores here
    db.session.commit()

    # create new user chores

    # get the date from the house and determine the actual start date
    init_sched_date = house.start_date

    # create a list of housemates and count the number to assign out to them
    housemates_list = House.query.get(house_id).users
    num_housemates = len(housemates_list)

    # use enumerate to create an index for each house chore that allows for easy assignment
    for index, house_chore in enumerate(house.house_chores):
        print "index: %s, house_chore: %s" % (index, house_chore)

        # while schedule start day (ie Sunday) != house chore day
        while datetime.datetime.strftime(init_sched_date,"%A") != house_chore.day: 
            init_sched_date += datetime.timedelta(days=1)

        # this is the first occurence of the chore
        first_sched_date = init_sched_date
        print "first_sched_date = ", first_sched_date

        print "int(house.num_weeks)", int(house.num_weeks)
        print "int(house_chore.week_freq)", int(house_chore.week_freq)

        # create user chores for each occurrence
        for i in range(int(house.num_weeks) / int(house_chore.week_freq)):
            due_date = first_sched_date + datetime.timedelta(days=((i)*(int(house_chore.week_freq)*7)))

            housemate = housemates_list[(index + i) % num_housemates]
            print "HOUSEMATE: ", housemate

            print "user_id: %s, chore_id: %s, due_date: %s" % (housemate.id, house_chore.chore.id, due_date.strftime("%A, %m/%d/%y"))

            new_userchore = UserChore(user_id=housemate.id, 
                                        chore_id=house_chore.chore.id,
                                        due_date=due_date)

            db.session.add(new_userchore)

    # commit new user_chores
    db.session.commit()

    return redirect("/calendar_view") # use this to conserve texts for testing
    # return redirect("/invite_housemates")     

@app.route("/invite_housemates", methods=['POST','GET'])
def invite_housemates():
    """Routed from create_house_pref view after create_user_chores to invite housemates"""

    # get list of housemates that isn't the admin
    housemates_list = User.query.filter(User.house_id==session['house_id'], User.is_admin==0).all()

    for housemate in housemates_list:
        message = "Chore Me Invitation :) https://a9dc1625.ngrok.io/"+str(housemate.id)
        client.messages.create(
            # to=housemate.phone, 
            to=MY_PHONE_NUMBER, #using this for testing purposes
            from_=MY_TWILIO_NUMBER,
            body=message)
        resp = twilio.twiml.Response()
        resp.message(message)
 
    return redirect("/calendar_view")



@app.route("/calendar_view", methods=['GET'])
def calendar_view():
    """Renders the calendar view of the user's house and chores assigned."""

    return render_template('calendar_view.html')


@app.route("/render_house_chores", methods=['POST'])
def render_house_chores():
    """Returns house chores through ajax call from calendar_view"""

    house = House.query.get(session['house_id']) 

    # create a dictionary with the date as a key and values as a list of tuples of user_chore data
    user_chores_dict = {}
    for user in house.users:
        for user_chore in UserChore.query.filter(UserChore.is_active==True, UserChore.user_id==user.id).all():
            print user_chore
            if user_chore.due_date.strftime("%Y-%m-%d") in user_chores_dict: 
                user_chores_dict[user_chore.due_date.strftime("%Y-%m-%d")].append((user_chore.chore.name, user_chore.user.username, user_chore.is_done, user_chore.id))
            else:
                user_chores_dict[user_chore.due_date.strftime("%Y-%m-%d")] = [(user_chore.chore.name, user_chore.user.username, user_chore.is_done, user_chore.id)]

    return jsonify(user_chores_dict)


@app.route("/personal_view", methods=['GET'])
def personal_view():
    """Renders the personal task list view of the user's assigned chores."""

    return render_template('personal_view.html')


@app.route("/render_personal_chores", methods=['POST'])
def render_personal_chores():
    """Returns personal chores through ajax call from personal_view"""

    user = User.query.get(session['user_id']) 

    user_chores_dict = {}
    for user_chore in user.user_chores:
        if user_chore.due_date.strftime("%m/%d/%y") in user_chores_dict:
            user_chores_dict[user_chore.due_date.strftime("%m/%d/%y")].append((user_chore.chore.name, user_chore.is_done, user_chore.id))
        else:
            user_chores_dict[user_chore.due_date.strftime("%m/%d/%y")] = [(user_chore.chore.name, user_chore.is_done, user_chore.id)]
    print user_chores_dict
    return jsonify(user_chores_dict)


@app.route("/chore_done", methods=['POST'])
def chore_done():
    """When chore is completed in personal view, update the database."""

    user_chore_id = request.form.get("hidden_personal_chore_input")
    user_chore = UserChore.query.get(user_chore_id)
    user_chore.is_done = True
    db.session.commit()

    return jsonify({"result": user_chore_id})



@app.route("/chore_undone", methods=['POST'])
def chore_undone():
    """When chore is unchecked in personal view, update the database."""

    user_chore_id = request.form.get("hidden_personal_chore_input")
    user_chore = UserChore.query.get(user_chore_id)
    user_chore.is_done = False
    db.session.commit()

    return jsonify({"result": user_chore_id})


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
            return redirect('/personal_view')


    except NoResultFound:
        flash("Username not recognized. Please re-enter or register below.")
        return redirect('/')


@app.route('/logout')
def logout():
    """Logout route that redirects to the homepage"""
    flash("Logged out")

    session['user_id'] = None
    session['house_id'] = None

    return redirect('/')


############################################################################## 

print "you are awesome"
 
if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    # DebugToolbarExtension(app)

    app.run(debug=True)