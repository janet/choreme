from twilio.rest import TwilioRestClient 
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db

import twilio.twiml
import os
 
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
 
 
# twilio credentials here 
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
 
@app.route("/", methods=['GET', 'POST'])
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



print "you are awesome"
 
if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(debug=True)