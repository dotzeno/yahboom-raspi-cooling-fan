import time
import os
import adafruit_ssd1306
import subprocess
import busio
import smbus
bus = smbus.SMBus(1)

from PIL import Image, ImageDraw, ImageFont
from board import SCL, SDA

hat_addr = 0x0d
rgb_off_reg = 0x07
fan_reg = 0x08
fan_state = 2
count = 0

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# 128x32 display with hardware I2C:
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

def setFanSpeed(speed):
    bus.write_byte_data(hat_addr, fan_reg, speed&0xff)

def setRGB( r, g, b):
        bus.write_byte_data(hat_addr, 0x00, 0xff)
        bus.write_byte_data(hat_addr, 0x01, r&0xff)
        bus.write_byte_data(hat_addr, 0x02, g&0xff)
        bus.write_byte_data(hat_addr, 0x03, b&0xff)
        
bus.write_byte_data(hat_addr,rgb_off_reg,0x00)
time.sleep(1)

def getCPULoadRate():
    f1 = os.popen("cat /proc/stat", 'r')
    stat1 = f1.readline()
    count = 10
    data_1 = []
    for i  in range (count):
        data_1.append(int(stat1.split(' ')[i+2]))
    total_1 = data_1[0]+data_1[1]+data_1[2]+data_1[3]+data_1[4]+data_1[5]+data_1[6]+data_1[7]+data_1[8]+data_1[9]
    idle_1 = data_1[3]

    time.sleep(1)

    f2 = os.popen("cat /proc/stat", 'r')
    stat2 = f2.readline()
    data_2 = []
    for i  in range (count):
        data_2.append(int(stat2.split(' ')[i+2]))
    total_2 = data_2[0]+data_2[1]+data_2[2]+data_2[3]+data_2[4]+data_2[5]+data_2[6]+data_2[7]+data_2[8]+data_2[9]
    idle_2 = data_2[3]

    total = int(total_2-total_1)
    idle = int(idle_2-idle_1)
    usage = int(total-idle)
    print("idle:"+str(idle)+"  total:"+str(total))
    usageRate =int(float(usage * 100/ total))
    print("usageRate:%d"%usageRate)
    return "CPU:"+str(usageRate)+"%"


def setOLEDshow():
# Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    CPU = getCPULoadRate()
    cmd = os.popen('vcgencmd measure_temp').readline()
    CPU_temp = cmd.replace("temp=","temp:").replace("'C\n","C")
    global g_temp
    g_temp = float(cmd.replace("temp=","").replace("'C\n",""))
    cmd = "free -m | awk 'NR==2{printf \"RAM:%.2f/%.2fGB %.1f%%\", $3/1024,$2/1024,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk:%.1f/%.1fGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "ip addr show | awk '/inet.*brd/{print $NF}' | head -1"
    NIC = subprocess.check_output(cmd, shell = True ).decode("utf-8").strip()
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True ).decode("utf-8")

    # Write two lines of text.
    draw.text((x, top), str(CPU), font=font, fill=255)
    draw.text((x+56, top), str(CPU_temp), font=font, fill=255)
    draw.text((x, top+8), str(MemUsage),  font=font, fill=255)
    draw.text((x, top+16), str(Disk),  font=font, fill=255)
    draw.text((x, top+24), str(NIC)+":"+str(IP),  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(0.1)

while True:
    setOLEDshow()
    print("g_temp:"+str(g_temp)) 
    if g_temp <= 45:
        setFanSpeed(0x00)
        setRGB( 0x00, 0x00, 0xff)
    elif g_temp <= 47:
        setFanSpeed(0x04)
        setRGB( 0x1e, 0x90, 0xff)
    elif g_temp <= 49:
        setFanSpeed(0x06)
        setRGB( 0x00, 0xbf, 0xff)
    elif g_temp <= 51:
        setFanSpeed(0x08)
        setRGB( 0x5f, 0x9e, 0xa0)
    elif g_temp <= 53:
        setFanSpeed(0x09)
        setRGB( 0xff, 0xff, 0x00)
    elif g_temp <= 55:
        setFanSpeed(0x09)
        setRGB( 0xff, 0xd7, 0x00)
    elif g_temp <= 57:
        setFanSpeed(0x09)
        setRGB( 0xff, 0xa5, 0x00)
    elif g_temp <= 59:
        setFanSpeed(0x09)
        setRGB( 0xff, 0x8c, 0x00)
    elif g_temp <= 61:
        setFanSpeed(0x09)
        setRGB( 0xff, 0x45, 0x00)
    else:
        setFanSpeed(0x01)
        setRGB( 0xff, 0x00, 0x00)
    
    time.sleep(.5)
