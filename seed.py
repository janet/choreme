"""Utility file to seed choreme database with dummy data from seed_data file"""

from model import User, House, Schedule, HouseChore, DayOfWeek, WeekFreq, Chore, UserChore
from model import connect_to_db, db
from server import app
from datetime import datetime

def load_users():
    """Load users from u.user into database."""
    seed_file = open("seed_data/user")
    for line in seed_file:  
        line = line.rstrip()
        seed_line = line.split("|")
        
        new_user = User(
            house_id=int(seed_line[0]),
            email=seed_line[1],
            first_name=seed_line[2],
            password=seed_line[3],
            phone=int(seed_line[4]),
            is_admin=bool(seed_line[5])
            )
        db.session.add(new_user)
    db.session.commit()


def load_houses():
    """Load houses from house into database."""
    seed_file = open("seed_data/house")
    for line in seed_file:
        line = line.rstrip()
        seed_line = line.split(" ")
        
        new_house = House(
            house_name=seed_line[0]
            )
        db.session.add(new_house)
    db.session.commit()

def load_schedule():
    """Load sched from sched into database."""
    seed_file = open("seed_data/sched")
    for line in seed_file:
        line = line.rstrip()
        seed_line = line.split("\t")
        
        new_sched = Schedule(
            house_id=int(seed_line[0]),
            end_date=datetime.strptime(seed_line[1], "%w, %m/%d/%y")
            )
        db.session.add(new_sched)
    db.session.commit()


def load_day_of_week():
    """Load day_of_week ref table from dow into database."""
    seed_file = open("seed_data/day_of_week")
    for line in seed_file:
        line = line.rstrip()
        seed_line = line.split("\t")
        
        new_dow = DayOfWeek(
            dow_name=seed_line[0])

        db.session.add(new_dow)
    db.session.commit()    

def load_week_freq():
    """Load week_freq ref table from week_freq into database."""
    seed_file = open("seed_data/week_freq")
    for line in seed_file:
        line = line.rstrip()
        seed_line = line.split("\t")
        
        new_week_freq = WeekFreq(
            week_freq_name=seed_line[0],
            week_freq_value=seed_line[1])

        db.session.add(new_week_freq)
    db.session.commit()    

def load_house_chore():
    """Load house_chore from house_chore into database."""
    seed_file = open("seed_data/house_chore")
    for line in seed_file:
        line = line.rstrip()
        seed_line = line.split("\t")

        new_house_chore = HouseChore(
            schedule_id=int(seed_line[0]),
            chore_id=int(seed_line[1]),
            dow=seed_line[2],
            week_freq=seed_line[3]
            )
        db.session.add(new_house_chore)
    db.session.commit()

def load_chore():
    """Load chores from chore into database."""
    seed_file = open("seed_data/chore")
    for line in seed_file:
        line = line.rstrip()
        seed_line = line.split("\t")
        
        new_chore = Chore(
            chore_name=seed_line[0])

        db.session.add(new_chore)
    db.session.commit() 

def load_user_chore():
    """Load user chores from user_chore into database."""
    seed_file = open("seed_data/user_chore")
    for line in seed_file:
        line = line.rstrip()
        seed_line = line.split("\t")
        
        new_user_chore = UserChore(
            user_id=int(seed_line[0]),
            house_chore_id=int(seed_line[1]),
            due_date=datetime.strptime(seed_line[2], "%w, %m/%d/%y"))

        db.session.add(new_user_chore)
    db.session.commit() 




if __name__ == "__main__":
    connect_to_db(app)
    db.drop_all()
    db.create_all()

    # import pdb; pdb.set_trace()

    load_houses()
    load_users()
    load_schedule()
    load_day_of_week()
    load_week_freq()
    load_house_chore()
    load_chore()
    load_user_chore()