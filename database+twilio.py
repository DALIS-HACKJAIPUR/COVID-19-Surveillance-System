#integrating database with twilio in order to send message to the phone number extracted from QR code

import sqlite3


conn = sqlite3.connect('Entries.db') #making table Entries 
c = conn.cursor() #created cursor to work with table
c.execute("CREATE TABLE entries (first text, plate text, phone text, number_fine integer, is_visited integer)")
#Adding column is_visited in order to make sure the person doesn't have to pay fine twice in same day.


#Creating user class in order to add user efficiently
class User():

  def __init__(self, first, plate, phone, number_fine, is_visited):
    self.first = first
    self.plate = plate
    self.phone = phone
    self.number_fine = number_fine
    self.is_visited = is_visited

#Dummy users
user1 = User('Ritik', 'MP 09 BC1937', '9174333707', 0, 0) #initializing is_visited to 0
user2 = User('Sourav', 'MH 02 PD1120', '8989209896', 0, 0)

#Adding these dummy users into the database
with conn:
  c.execute("INSERT INTO Entries VALUES (:first, :plate, :phone, :number_fine, :is_visited)", {'first':user1.first, 'plate':user1.plate, 'phone':user1.phone, 'number_fine':user1.number_fine, 'is_visited':user1.is_visited})
  c.execute("INSERT INTO Entries VALUES (:first, :plate, :phone, :number_fine, :is_visited)", {'first':user2.first, 'plate':user2.plate, 'phone':user2.phone, 'number_fine':user2.number_fine, 'is_visited':user2.is_visited})

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
    c.execute("SELECT number_fine, is_visited FROM Entries WHERE phone=:phone", {'phone':ph}) #selecting both number_fine and is_visited from the database
    li = c.fetchall()[0] #li is list of [number_fine, is_visited]
    if(li[0]==0 and li[1]==0): #if both number_fine and is_visited are 0 
    #both zero means person is being scanned for first time.

    c.execute("UPDATE Entries SET number_fine = :number_fine, is_visited = :is_visited WHERE phone = :phone",{'number_fine':1, 'is_visited':1,'phone':ph})
    print("First Warning")
    #Twilio warning message
    client.messages.create(
                            to = "+91"+ph,
                            from_ = "+12513222811",
                            body = "This is your first warning, as you were not wearing a mask today while driving"
                            )

    elif(li[0]!=0 and li[1]==0): #if number_fine is not 0 but is_visited is 0
    #This situation indicates that a person has been warned before but not warned today, hence pay the fine.

    c.execute("UPDATE Entries SET is_visited = :is_visited WHERE phone = :phone",{'is_visited':1,'phone':ph})
    print("You have to give fine")
    #Twilio fine message
    client.messages.create(
                            to = "+91"+ph,
                            from_ = "+12513222811",
                            body = "This is a message for you stating your fine, as you were not wearing a mask today while driving even after a final warning"
                            )

    else: #if number fine is not 0 and is_visited is also not 0
    #this situation corresponds the person has been encountered same day before. Hence *Final Warning*

    c.execute("SELECT day FROM Entries WHERE phone=:phone", {'phone':ph})
    c.execute("UPDATE Entries SET is_visited = :is_visited Where phone = :phone", {'is_visited':0, 'phone':ph})
    print("No Mask found again today (Final Warning)")
    #Twilio Final Warning Message
    client.messages.create(
                        to = "+91"+ph,
                        from_ = "+12513222811",
                        body = "This is your final warning, as you were not wearing a mask today while driving. You have to give fine after this."
                        )
    
