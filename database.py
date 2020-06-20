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