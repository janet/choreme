"""Utility file to seed choreme database with dummy data from seed_data file"""

from model import User, House, HouseChore, Chore, UserChore
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
            username=seed_line[1],
            password=seed_line[2],
            phone=int(seed_line[3]),
            is_admin=bool(seed_line[4])
            )
        db.session.add(new_user)
    db.session.commit()


def load_houses():
    """Load houses from house into database."""
    seed_file = open("seed_data/house")
    for line in seed_file:
        line = line.rstrip()
        seed_line = line.split("\t")
        
        new_house = House(
            name=seed_line[0],
            start_date=datetime.strptime(seed_line[1], "%w, %m/%d/%y"),
            num_weeks=seed_line[2]
            )
        db.session.add(new_house)
    db.session.commit()

def load_house_chore():
    """Load house_chore from house_chore into database."""
    seed_file = open("seed_data/house_chore")
    for line in seed_file:
        line = line.rstrip()
        seed_line = line.split("\t")

        new_house_chore = HouseChore(
            house_id=int(seed_line[0]),
            chore_id=int(seed_line[1]),
            day=seed_line[2],
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
            name=seed_line[0])

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
            chore_id=int(seed_line[1]),
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
    load_house_chore()
    load_chore()
    load_user_chore()