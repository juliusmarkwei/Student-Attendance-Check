import os, sys, uos
from machine import Pin, SPI
from mfrc522 import MFRC522
from time import sleep_ms


class RFIDHandler:
    # RFID pin setup
    sck = Pin(18, Pin.OUT)
    mosi = Pin(23, Pin.OUT)
    miso = Pin(19, Pin.OUT)
    spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
    sda = Pin(5, Pin.OUT)
    
    def __init__(self, spi=spi, sda=sda):
        self.rdr = MFRC522(spi, sda)


    def ensure_data_folder(self):
        # Check if the 'data' folder exists, if not, create it
        if not sys.path('data'):
            os.mkdir('data')

    def read_rfid(self):
        print("Swipe card onto scanner")
        uid = ""
        while uid == "":
            (stat, tag_type) = self.rdr.request(self.rdr.REQIDL)
            if stat == self.rdr.OK:
                (stat, raw_uid) = self.rdr.anticoll()
                if stat == self.rdr.OK:
                    uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    sleep_ms(100)
        return uid
    
    def take_index_number(self):
        return input("Enter index number: ")
        
        
    def store_data(self, uid):
        index = self.take_index_number()
        if not self.is_info_in_file(uid, index):
            with open("data/database.csv", "a") as f:
                f.write(uid + " - " + index + "\n")
                sleep_ms(2000)
                print("\nUser already in database")
                return
        print("Added successfully")
        


    def is_info_in_file(self, uid, index):
        f = open("data/database.csv", "w+")
        for line in f.readlines():
            data_id, data_index = line.split(" - ")
            if data_id == uid or data_index == index:
                return True
        return False


    def remove_user_from_database(self, uid):
        print("Removing user from database!")
        sleep_ms(2000)
        lines = []
        with open("data/database.csv", "w+") as f:
            lines = f.readlines()

        with open("data/database.csv", "w+") as f:
            for line in lines:
                data_id, data_index = line.split(" - ")
                if data_id != uid or data_index != index:
                    f.write(uid + " - " + index + "\n")
                else:
                    user_removed = data_index
        print("\nRemoved successfully")

# Initialize RFID handler
rfid_handler = RFIDHandler()

# Read RFID
uid = rfid_handler.read_rfid()

# Store ID
# rfid_handler.store_data(uid)

# Remove ID
rfid_handler.remove_user_from_database(uid)


