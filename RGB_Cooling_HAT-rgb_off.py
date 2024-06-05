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
fan_reg = 0x08
rgb_off_reg = 0x07
Max_LED = 3

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
# path = os.path.dirname(__file__) + '/'
# font = ImageFont.truetype(path + 'Minecraftia.ttf', 8)

def setFanSpeed(speed):
    bus.write_byte_data(hat_addr, fan_reg, speed&0xff)

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
    #print("idle:"+str(idle)+"  total:"+str(total))
    usageRate =int(float(usage * 100/ total))
    #print("usageRate:%d"%usageRate)
    return "CPU:"+str(usageRate)+"%"

def getNetwork():
    cmd = "ip addr show | awk '/inet.*brd/{print $NF}' | head -1"
    NIC = subprocess.check_output(cmd, shell = True ).decode("utf-8").strip()
    if len(NIC)==0:
        return "No Active NIC Found"
    elif len(NIC) != 0:
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True ).decode("utf-8")
        return str(NIC)+":"+str(IP)

def setOLEDshow():
# Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    CPU = getCPULoadRate()
    cmd = os.popen('cat /sys/class/thermal/thermal_zone*/temp').readline().strip()
    global g_temp
    if len(cmd) == 5: 
        CPU_TEMP=cmd[:2]+"."+cmd[2:3]
        g_temp = int(cmd[:2])
    else:
        CPU_TEMP=cmd[:3]+"."+cmd[3:4]
        g_temp = int(cmd[:2])
    CPU_TEMP=CPU_TEMP+"C"
    cmd = "free -m | awk 'NR==2{printf \"RAM:%.2f/%.2fGB %.0f%%\", $3/1024,$2/1024,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk:%.1f/%.1fGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    Network = getNetwork()

    # Write five lines of text.
    draw.text((x, top), str(CPU), font=font, fill=255)
    draw.text((x+56, top), str(CPU_TEMP), font=font, fill=255)
    draw.text((x, top+8), str(MemUsage),  font=font, fill=255)
    draw.text((x, top+16), str(Disk),  font=font, fill=255)
    draw.text((x, top+24), str(Network),  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(1)

def setRGB(num, r, g, b):
    bus.write_byte_data(hat_addr, 0x00, num&0xff)
    bus.write_byte_data(hat_addr, 0x01, r&0xff)
    bus.write_byte_data(hat_addr, 0x02, g&0xff)
    bus.write_byte_data(hat_addr, 0x03, b&0xff)

while True:
    bus.write_byte_data(hat_addr, rgb_off_reg, 0x00)
    time.sleep(1)
    setRGB(Max_LED, 0, 0, 0)
    setOLEDshow()
    if g_temp <= 45:
        setFanSpeed(0x00)
    elif g_temp <= 47:
        setFanSpeed(0x04)
    elif g_temp <= 49:
        setFanSpeed(0x06)
    elif g_temp <= 51:
        setFanSpeed(0x08)
    elif g_temp <= 53:
        setFanSpeed(0x09)
    elif g_temp <= 55:
        setFanSpeed(0x09)
    elif g_temp <= 57:
        setFanSpeed(0x09)
    elif g_temp <= 59:
        setFanSpeed(0x09)
    elif g_temp <= 61:
        setFanSpeed(0x09)
    else:
        setFanSpeed(0x01)
    
    time.sleep(1)
