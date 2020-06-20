#Adding twilio API functionalities

#to check, we need to install twilio ; pip install twilio
from twilio.rest import Client #imported twilio Client
acc_sid = "AC5c4ca1c5873e7cbfbafc5xxxxxxxx4f13" #dummy number acc_sid
auth_token = "32ca306f7ddc1ec174f1xxxxxxxx90a1" #dummy number auth_token

client = Client(acc_sid, auth_token) #creation of client