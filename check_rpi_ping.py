import subprocess
import datetime

from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from inky import InkyPHAT

#########---{ check_rpi_ping.py }---##############
#
# Check my RPi:s ping and display on my InkyPhat
#
# By Jonas Wadsten, oct 2019
#
# Rev 1: Added rotation of display, 21 dec 2019
#
############################################################

now = datetime.datetime.now()

inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)

font12 = ImageFont.truetype(FredokaOne, 12)
font14 = ImageFont.truetype(FredokaOne, 14)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

# function to ping ip-addresses
def pinging(ip_adress):
    res = subprocess.call(['ping', '-c', '3', ip_adress])
    if res == 0:

        print(now.strftime("%Y-%m-%d %H:%M"), "ping to" , ip_adress, "OK")
        return res
    elif res == 2:
        print(now.strftime("%Y-%m-%d %H:%M"), "no response from", ip_adress)
        return res
    else:
        print(now.strftime("%Y-%m-%d %H:%M"), "ping to", ip_adress, "failed!")
        return res

printtime = now.strftime("%Y-%m-%d | kl %H:%M")
w, h = font12.getsize(printtime)
x = (inky_display.WIDTH / 2) - (w / 2)
draw.text((x,1), printtime , inky_display.BLACK, font12)


# prints the rpi status on the left side of the screen
rpis = ["131", "200", "220", "230", "231", "234"]
rpi_name = ["134.Tinker", "200.HA", "220.Inky", "230.MM2", "231.3DPrCam", "234.4inch"]
startpoint = 0
startname = -1
for ping in rpis:
    startpoint = startpoint + 12
    startname = startname +1
    rpiname = rpi_name[startname]
    if (pinging ("192.168.68." + ping)) == 0:
        draw.text((1, startpoint), rpiname + " ", inky_display.BLACK, font12)
        draw.text((80, startpoint), "OK", inky_display.BLACK, font12)
    else:
        draw.text((1, startpoint), rpiname + " ", inky_display.BLACK, font12)
        draw.text((80, startpoint), "NO!", inky_display.RED, font12)


# prints the rpi status on the right side of the screen
rpis = ["116", "121", "124", "112", "128", "150"]
rpi_name = ["116.ArloCams", "121.Hue", "124.Telldus", "112.HPrint", "128.3DPrint", "150.Snlgy"]
startpoint = 0
startname = -1
for ping in rpis:
    startpoint = startpoint + 12
    startname = startname +1
    rpiname = rpi_name[startname]
    if (pinging ("192.168.68." + ping)) == 0:
        draw.text((110, startpoint), rpiname + " ", inky_display.BLACK, font12)
        draw.text((190, startpoint), "OK", inky_display.BLACK, font12)
    else:
        draw.text((110, startpoint), rpiname + " ", inky_display.BLACK, font12)
        draw.text((190, startpoint), "NO!", inky_display.RED, font12)

#rotates the image 180 degrees
flipped = img.rotate(180)
inky_display.set_image(flipped)
inky_display.show()

