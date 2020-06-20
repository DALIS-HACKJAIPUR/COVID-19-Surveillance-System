#integrating database with twilio in order to send message to the phone number extracted from QR code

import sqlite3
import time #importing time as it gives us current day counted from initial day.
            #Calculating 24 hrs from difference of days is best way as there are least chances of errors.

conn = sqlite3.connect('Entries.db') #making table Entries 
c = conn.cursor() #created cursor to work with table
c.execute("CREATE TABLE entries (first text, plate text, phone text, number_fine integer, is_visited integer, day integer)")
#Adding column day in order to reset is_visited on appropiate time.


#Creating user class in order to add user efficiently
class User():

  def __init__(self, first, plate, phone, number_fine, is_visited):
    self.first = first
    self.plate = plate
    self.phone = phone
    self.number_fine = number_fine
    self.is_visited = is_visited
    self.day = None

#Dummy users
user1 = User('Ritik', 'MP 09 BC1937', '9174333707', 0, 0) #initializing is_visited to 0
user2 = User('Sourav', 'MH 02 PD1120', '8989209896', 0, 0)

#Adding these dummy users into the database
with conn:
  c.execute("INSERT INTO Entries VALUES (:first, :plate, :phone, :number_fine, :is_visited, :day)", {'first':user1.first, 'plate':user1.plate, 'phone':user1.phone, 'number_fine':user1.number_fine, 'is_visited':user1.is_visited, 'day':user1.day})
  c.execute("INSERT INTO Entries VALUES (:first, :plate, :phone, :number_fine, :is_visited, :day)", {'first':user2.first, 'plate':user2.plate, 'phone':user2.phone, 'number_fine':user2.number_fine, 'is_visited':user2.is_visited, 'day':user2.day})

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
    c.execute("SELECT number_fine, is_visited FROM Entries WHERE phone=:phone", {'phone':ph})
    li = c.fetchall()[0]
    if(li[0]==0 and li[1]==0):#if both number_fine and is_visited are 0 
    #both zero means person is being scanned for first time.
        day_now = time.localtime(time.time())[7] #Extracting day from struct of time (CURRENT DAY)
        c.execute("UPDATE Entries SET number_fine = :number_fine, is_visited = :is_visited, day = :day WHERE phone = :phone",{'number_fine':1, 'is_visited':1, 'day':day_now, 'phone':ph})
        #Also storing day in DB for future reference.
        print("First Warning")

        #Twilio warning message
        client.messages.create(
                                to = "+91"+ph,
                                from_ = "+12513222811",
                                body = "This is your first warning, as you were not wearing a mask today while driving"
                                )

    elif(li[0]!=0 and li[1]==0): #if number_fine is not 0 but is_visited is 0
    #This situation indicates that a person has been warned before but not warned today, hence pay the fine.
        day_now = time.localtime(time.time())[7]#Extrating Current Day and storing in db for future.
        c.execute("UPDATE Entries SET is_visited = :is_visited, day = :day WHERE phone = :phone",{'is_visited':1, 'day':day_now, 'phone':ph})
        print("You have to give fine")
        client.messages.create(
                                to = "+91"+ph,
                                from_ = "+12513222811",
                                body = "This is a message for you stating your fine, as you were not wearing a mask today while driving even after a final warning"
                                )
    else:
    #if number fine is not 0 and is_visited is also not 0
    #means person has been encountered before.
        c.execute("SELECT day FROM Entries WHERE phone=:phone", {'phone':ph})
        client_day = c.fetchall()[0][0] #Extracting the day when he was encountered last time.
        now_day = time.localtime(time.time())[7] #Extracting current day
        if(now_day <= client_day): #if current day is greater, *MORE THAN 24 hrs of TIME!*
            print("Already given fine for today!") #24 hrs not passed and he has already given fine.

        else: #24 hrs have passed and he has to give fine.
            c.execute("UPDATE Entries SET is_visited = :is_visited Where phone = :phone", {'is_visited':0, 'phone':ph})
            print("No Mask found again today (Final Warning)")
            client.messages.create(
                                to = "+91"+ph,
                                from_ = "+12513222811",
                                body = "This is your final warning, as you were not wearing a mask today while driving. You have to give fine after this."
                                )