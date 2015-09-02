# Chore Me

Chore Me is a chore scheduling web application used to distribute chores evenly among housemates!

It uses the following tech stack:
  - Twilio API
  - Flask - web framework
  - Python - backend
  - Sqlite - database
  - SQLAlchemy - ORM
  - Datetime
  - Javascript / Jquery
  - Bootstrap
  - [Clndr.js](http://kylestetz.github.io/CLNDR/)
  - Moment.js
  - Jinja

# User Flow

> Users belong to Houses. 
> Each House has its own chore requirements (Vacuuming once a week on Sundays).
> Chores can be rescheduled to add/remove new users in a house as well as change the chore requirements :)

### Create House Prefs
![house preferences](https://raw.githubusercontent.com/janet/choreme/master/static/img/readme-house-pref.png)
* Users can add/remove new housemates in the housemates section
* Users can select chores for their house by clicking the plus button
* Once users click on the chore in the selected chores table, a modal window will set the frequency

![modal window for chores requirements](https://raw.githubusercontent.com/janet/choreme/master/static/img/readme-modal.png)

### Calendar View
![Calendar View](https://raw.githubusercontent.com/janet/choreme/master/static/img/readme-calendar-view-selected.png)
* Users can view all chores assigned for their household in the Calendar View
* When users click on the day marked with an icon of a chore, the table on the right renders to show (Chore, Assigned, Status)

### Personal View
![Personal View](https://raw.githubusercontent.com/janet/choreme/master/static/img/readme-personal-view.png)
* Users also have access to their own list of tasks in the Personal View
* Here they can check chores once complete to update the status in the Calendar View

### Twilio API
* Invited users will receive a text message with a direct link to a special invited user registration page
![Invite](https://raw.githubusercontent.com/janet/choreme/master/static/img/readme-twilio-invite.png)
* Alerts will also be sent on the day chores are due to remind users 
![Alert](https://raw.githubusercontent.com/janet/choreme/master/static/img/readme-twilio-alert.png)

**Contact Info: Janet Kenmotsu**
- https://www.linkedin.com/in/janetkenmotsu


