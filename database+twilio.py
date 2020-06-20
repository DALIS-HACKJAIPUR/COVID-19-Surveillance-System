#integrating database with twilio in order to send message to the phone number extracted from QR code

import sqlite3


conn = sqlite3.connect('Entries.db') #making table Entries 
c = conn.cursor() #created cursor to work with table
c.execute("CREATE TABLE entries (first text, plate text, phone text, number_fine integer)") #creating columns in table for first name, no plate, phone number and number fine.


#Creating user class in order to add user efficiently
class User():

  def __init__(self, first, plate, phone, number_fine):
    self.first = first
    self.plate = plate
    self.phone = phone
    self.number_fine = number_fine

#Dummy users
user1 = User('Ritik', 'MP 09 BC1937', '9174333707', 0)
user2 = User('Sourav', 'MH 02 PD1120', '8989209896', 0)

#Adding these dummy users into the database
with conn:
  c.execute("INSERT INTO Entries VALUES (:first, :plate, :phone, :number_fine)", {'first':user1.first, 'plate':user1.plate, 'phone':user1.phone, 'number_fine':user1.number_fine})
  c.execute("INSERT INTO Entries VALUES (:first, :plate, :phone, :number_fine)", {'first':user2.first, 'plate':user2.plate, 'phone':user2.phone, 'number_fine':user2.number_fine})

#Confirming addition of Users.
with conn:
  c.execute("SELECT * FROM Entries")
  print(c.fetchall())



#to check, we need to install twilio ; pip install twilio
from twilio.rest import Client #imported twilio Client
acc_sid = "AC5c4ca1c5873e7cbfbafc5xxxxxxxx4f13" #dummy number acc_sid
auth_token = "32ca306f7ddc1ec174f1xxxxxxxx90a1" #dummy number auth_token

client = Client(acc_sid, auth_token) #creation of client

#dummy phone number.. orginial will be extracted from the QR Code scanned.
ph='9174333707'

#opening DB
with conn:
  c.execute("SELECT number_fine FROM Entries WHERE phone=:phone", {'phone':ph}) #selecting number_fine column from row with dummy phone number
  if((c.fetchall()[0][0])==0):
    c.execute("UPDATE Entries SET number_fine = :number_fine WHERE phone = :phone",{'number_fine':1, 'phone':ph})
    print("First Warning") #if this is the first time, he was caught, giving warning,
     #Sending message with TWILIO API
    client.messages.create(
                            to = "+91"+ph,
                            from_ = "+12513222811",
                            body = "This is your first warning, as you were not wearing a mask today while driving"
                          )
                         
  else:
    print("You have to give fine") #if number_fine is not 0, its more than first time he has broken
    #Sending message with TWILIO API
    client.messages.create(
                            to = "+91"+str(ph),
                            from_ = "+12513222811",
                            body = "This is a message for you stating your fine, as you were not wearing a mask today while driving for a second or more than second time"
                          )