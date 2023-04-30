from time import sleep_ms
from machine import Pin, SPI
from mfrc522 import MFRC522

sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.OUT)
spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
sda = Pin(5, Pin.OUT)

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
    
def sdcard():
    UID = read_rfid()
    index = input("Enter index number : ")
    with open("/file.csv", 'a') as f:
            print("{}, {}".format(UID,index))
            f.write("{}, {}\n".format(UID,index))
            print("worked successfully")
            
sdcard()