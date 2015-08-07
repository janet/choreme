from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

##############################################################################

class User(db.Model):
    """User information"""

    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.house_id'), nullable=True)
    username = db.Column(db.String(64), nullable=True, unique=True)
    password = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.Integer, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    # define a relationship to House
    house = db.relationship("House",
                           backref=db.backref("users", order_by=user_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User user_id=%s username=%s>" % (self.user_id, self.username)

class House(db.Model):
    """House information"""

    __tablename__ = "house"

    house_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    house_name = db.Column(db.String(64), nullable=False, unique=True)
    mascot_img = db.Column(db.String(500), nullable=True) # 500 limit in case i 
	# want to do img urls and they are long

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<House house_id=%s house_name=%s>" % (self.house_id, self.house_name)
    
class Schedule(db.Model):
    """Schedule for a house. Has the end date of the schedule to keep track of whether it is the current schedule"""

    __tablename__ = "schedule"

    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.house_id'), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    schedule_length = db.Column(db.Integer, db.ForeignKey('schedule_length.sched_len_value'), nullable=False)

    # define a relationship to House
    house = db.relationship("House",
                           backref=db.backref("schedules", order_by=schedule_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Schedule schedule_id=%s end_date=%s>" % (self.schedule_id, self.end_date)

class ScheduleLength(db.Model):
    """Reference Table for schedule length and holds month to week conversion."""

    __tablename__ = "schedule_length"

    sched_len_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sched_len_value = db.Column(db.Integer, nullable=False)
    sched_len_in_weeks = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<ScheduleLength sched_len_id=%s sched_len_value=%s sched_len_in_weeks=%s>" % (self.sched_len_id, self.sched_len_value, self.sched_len_in_weeks)

class HouseChore(db.Model):
    """House chore with house preferred frequency & due date"""

    __tablename__ = "house_chore"

    house_chore_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.schedule_id'), nullable=False)
    chore_id = db.Column(db.Integer, db.ForeignKey('chore.chore_id'), nullable=False)
    dow = db.Column(db.String(9), db.ForeignKey('day_of_week.dow_name'), nullable=False)
    week_freq = db.Column(db.Integer, db.ForeignKey('week_freq.week_freq_value'), nullable=False) # week_freq(name : value) ex: (weekly:1, biweekly:2)

    # define a relationship to Schedule
    schedule = db.relationship("Schedule",
                           backref=db.backref("house_chores", order_by=house_chore_id))

    # define a relationship to Chore
    chore = db.relationship("Chore",
                           backref=db.backref("house_chores", order_by=house_chore_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<HouseChore house_chore_id=%s dow=%s week_freq=%s>" % (self.house_id, self.dow, self.week_freq)
    
class DayOfWeek(db.Model):
    """Reference Table for day of the week."""

    __tablename__ = "day_of_week"

    dow_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dow_name = db.Column(db.String(9), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<DayOfWeek dow_id=%s dow_name=%s>" % (self.dow_id, self.dow_name)

class WeekFreq(db.Model):
    """Reference Table for week frequency. Week frequency is an integer value from 1-4 and occurs once per n weeks."""

    __tablename__ = "week_freq"

    week_freq_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    week_freq_name = db.Column(db.String(20), nullable=False)
    week_freq_value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<WeekFreq week_freq_id=%s week_freq_name=%s>" % (self.week_freq_id, self.week_freq_name)

class Chore(db.Model):
    """Generic chore object"""

    __tablename__ = "chore"

    chore_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chore_name = db.Column(db.String(64), nullable=False)
    chore_icon = db.Column(db.String(500), nullable=True)  #500 limit in case i want to do img urls and they are long

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Chore chore_id=%s chore_name>" % (self.chore_id, self.chore_name)

class UserChore(db.Model):
    """Chore that is assigned to a user with a due date"""

    __tablename__ = "user_chore"

    user_chore_id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    house_chore_id = db.Column(db.Integer, db.ForeignKey('house_chore.house_chore_id'), nullable=False)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    due_date = db.Column(db.DateTime, nullable=False)

    # define a relationship to HouseChore
    house_chore = db.relationship("HouseChore",
                           backref=db.backref("user_chores", order_by=user_chore_id))

    # define a relationship to Chore
    user = db.relationship("User",
                           backref=db.backref("user_chores", order_by=user_chore_id))


    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<UserChore user_chore_id=%s is_done=%s due_date=%s>" % (self.user_chore_id, self.is_done, self.due_date)




    
##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///choreme.db'
    # app.config['SQLALCHEMY_RECORD_QUERIES'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from run import app
    connect_to_db(app)
    print "Connected to DB."