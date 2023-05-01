from time import sleep
from ST7735 import Display, color565
from machine import Pin, SPI
import fonts.sysfont as sysfont
import fonts.arial10 as arial10
import fonts.courier20 as courier20
import fonts.freesans20 as freesans20
import fonts.EspressoDolce18x24 as EspressoDolce18x24

sck = Pin(18)
miso= Pin(19)
mosi= Pin(23)
SPI_CS = 26
SPI_DC = 5
spi = SPI(2, baudrate=32000000, sck=sck, mosi=mosi, miso=miso)

display = Display(spi,SPI_CS,SPI_DC)

def test_text():
    display.clear()
    display.draw_text(10, 117, 'User in database',  arial10, Display.GREEN,landscape=True)
    display.draw_text(30, 127, 'Index:PS/ITC/20/0190',  arial10, Display.GREEN,landscape=True)
              


test_text()
sleep(10)
display.cleanup()


