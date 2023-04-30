from time import sleep_ms
from machine import Pin, SPI
from mfrc522 import MFRC522

# RFID pin setup
sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.OUT)
spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
sda = Pin(5, Pin.OUT)

# Function to read RFID UID with the scanner (return UID)
def read_rfid():
    uid = ""
    while uid == "":
        rdr = MFRC522(spi, sda)
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                sleep_ms(100)
    return uid

# Function to write new user to database
def sdwrite():
    print("Write to database")
    UID = read_rfid()
    if not isStored(UID):
        index = input("Enter index number : ")
        with open("/file.csv", 'a') as f:
                f.write("{}, {}\n".format(UID,index))
                print("{} added to database!".format(index))
    else:
        print("User already in database!")
           
# Function to check if user data is stored in database
def isStored(given_uid):
    uid, index = go_through(given_uid)
    return given_uid == uid

#Function to go through database and return id and index
def go_through(uid):
    with open("/file.csv", 'r') as f:
        while True:
            userInfo = f.readline()
            if userInfo:
                userUID, userIndex = userInfo.split(", ")
                userIndex = userIndex.strip()
            else:
                return "", ""
            
            if userUID == uid:
                return userUID, userIndex

# Function to validate user by checking through database
def check_user():
    userId = read_rfid()
    uid, index = go_through(userId)
    return index if index != "" else "User not found!"

# test
for i in range(3):
    sdwrite()
    
for i in range(2):
    print(check_user())