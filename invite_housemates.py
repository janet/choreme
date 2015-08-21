import os

from twilio.rest import TwilioRestClient 

from server import client, MY_TWILIO_NUMBER, MY_PHONE_NUMBER
 
client.messages.create(
	to=MY_PHONE_NUMBER, 
	from_=MY_TWILIO_NUMBER, 
	body="you are awesome",  
)

print "you are awesome"