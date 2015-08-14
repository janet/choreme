from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

##############################################################################

class User(db.Model):
    """User information"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=True)
    username = db.Column(db.String(64), nullable=True, unique=True)
    password = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.Integer, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    # define a relationship to House
    house = db.relationship("House",
                           backref=db.backref("users", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User user_id=%s username=%s>" % (self.id, self.username)

class House(db.Model):
    """House information"""

    __tablename__ = "house"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now()) 
    num_weeks = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<House house_id=%s house_name=%s>" % (self.id, self.name)

class HouseChore(db.Model):
    """House chore with house preferred frequency & due date"""

    __tablename__ = "house_chore"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=False)
    chore_id = db.Column(db.Integer, db.ForeignKey('chore.id'), nullable=False)
    day = db.Column(db.String(9), nullable=False)
    week_freq = db.Column(db.Integer, nullable=False) 

    # define a relationship to Schedule
    house = db.relationship("House",
                           backref=db.backref("house_chores", order_by=id))

    # define a relationship to Chore
    chore = db.relationship("Chore",
                           backref=db.backref("house_chores", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<HouseChore house_chore_id=%s day=%s week_freq=%s>" % (self.id, self.day, self.week_freq)

class Chore(db.Model):
    """Generic chore object"""

    __tablename__ = "chore"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    icon = db.Column(db.String(500), nullable=True)  #500 limit in case i want to do img urls and they are long

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Chore chore_id=%s chore_name=%s>" % (self.id, self.name)

class UserChore(db.Model):
    """Chore that is assigned to a user with a due date"""

    __tablename__ = "user_chore"

    id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chore_id = db.Column(db.Integer, db.ForeignKey('chore.id'), nullable=False)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    due_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # define a relationship to HouseChore
    chore = db.relationship("Chore",
                           backref=db.backref("user_chores", order_by=id))

    # define a relationship to Chore
    user = db.relationship("User",
                           backref=db.backref("user_chores", order_by=id))


    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<UserChore user_chore_id=%s is_done=%s due_date=%s active=%s>" % (self.id, self.is_done, self.due_date, self.active)




    
##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///choreme.db'
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # app.config['SQLALCHEMY_RECORD_QUERIES'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from run import app
    connect_to_db(app)
    print "Connected to DB."