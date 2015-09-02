import datetime
import unittest
import tempfile
import flask
import json
import sys
import os

from model import User, House, HouseChore, Chore, UserChore
from server import app, db
import seed

class ServerTestCase(unittest.TestCase):

    sys.stdout.write('Setting up temporary database...Done\n')
    def setUp(self):
        self.db_fd, self.db_filename = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + self.db_filename
        app.config['TESTING'] = True
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.test_client = app.test_client()
        db.app = app
        db.init_app(app)
        with app.app_context():
            db.create_all()
        seed.load_users()
        seed.load_houses()
        seed.load_house_chore()
        seed.load_chore()
        seed.load_user_chore()

    def login(self, client):
        return client.get('/process_login', data=dict(
                username="janet",
                password="password"
                ), follow_redirects=True)

    def test_login(self):
        """Checks that a user is in session after login with correct credentials."""

        sys.stdout.write('Testing login handler...')
        with app.test_client() as c:
            self.login(c)
            assert User.query.filter(User.username=='janet').one().id == 1

    def test_database_seed(self):
        """Ensures that the database seed file is functioning as expected."""

        sys.stdout.write('Testing database seed process...')
        user = User.query.get(1)
        house = House.query.get(1)
        assert user.username == "janet"
        assert house.name == "best_house"

    def test_create_user_chore(self):
        """Ensures that user chores are created as expected based on user inputs."""

        sys.stdout.write('Testing process of creating user chores...')

        # create test house for testing
        test_house = House(name="test house",
                        start_date=datetime.datetime.strptime("09/01/15", "%m/%d/%y"),
                        num_weeks=1)
        db.session.add(test_house)
        db.session.commit()

        # create test user for testing
        test_user = User(house_id=House.query.filter(House.name=="test house").one().id,
                         username="test user",
                         password="password",
                         phone="1234567",
                         is_admin=bool(1))
        db.session.add(test_user)

        # create test housechore for testing
        test_housechore = HouseChore(
                            house_id=House.query.filter(House.name=="test house").one().id,
                            chore_id=1, #vacuuming
                            day="Tuesday",
                            week_freq=1)
        db.session.add(test_housechore)
        db.session.commit()

        house = House.query.filter(House.name=="test house").one()

        # get the date from the house and determine the actual start date
        init_sched_date = house.start_date

        # create a list of housemates and count the number to assign out to them
        housemates_list = house.users
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

        assert UserChore.query.filter(UserChore.user_id==house.users[0].id).one().chore_id == 1

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_filename)
        sys.stdout.write("Done\n")

if __name__ == '__main__':
    unittest.main()