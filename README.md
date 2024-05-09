# YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT


I couldn't follow the [official](http://www.yahboom.net/study/RGB_Cooling_HAT) instructions or the instructions from [dogweather/yahboom-raspi-cooling-fan](https://github.com/dogweather/yahboom-raspi-cooling-fan) to get the OLED working so I did some research and made the necessary adjustments to get things working on 64-bit Raspbian OS.

I've adjusted the formatting to my liking and created a function in the script so that it can detect and show, in addition to the IP address, whether or not there's an active network adapter (and what that is) on the OLED display.

**Instructions for use with Raspberry Pi OS 64-bit**

**1. Enable I2C**

sudo [raspi-config](https://www.raspberrypi.org/documentation/configuration/raspi-config.md) and enable I2C. 

You may also enable VNC at this time if that is something you're more comfortable with (i.e. use VNC to remote into the device and use Chromium to download files onto the device).

**2. Download Scripts to Device**

Download RGB_Cooling_Hat.zip from YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT/4.Python programming/RGB_Cooling_HAT.zip (or click [here](https://github.com/YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT/blob/master/4.Python%20programming/RGB_Cooling_HAT.zip))

**2. Install Python3 Packages**

```bash
sudo pip3 install adafruit-circuitpython-ssd1306
```

**3. Run one or more of the Python scripts**

EXAMPLE 1:
If I want the Fan and RGB functions to be controlled by the device's temperature stats as well as the OLED functions enabled, then in three separate terminal windows, run:

```bash
python fan_temp.py
```

```bash
python rgb_temp.py
```

```bash
python oled.py
```

EXAMPLE 2:
If I want to use the AIO script (Fan, RGB and OLED functions enabled), then in one terminal window, run:

```bash
python RGB_Cooling_HAT.py
```

EXAMPLE 3:
If I want to use my custom AIO script (Fan and OLED functions enabled, RGB Off), then in one terminal window, run:

```bash
python RGB_Cooling_HAT-rgb_off.py
```

### Starting a script automatically when booting (same as dogweather's instructions)

This easiest way I've found so far is to add a line to root's crontab with `sudo crontab -e`:

```
@reboot /usr/bin/python3 /home/pi/src/yahboom-raspi-cooling-fan/RGB_Cooling_HAT.py
```

Multiple `@reboot` lines can be given. E.g., I'm currently running these two so that the lights simply stay default green and aren't changed:

```
@reboot /usr/bin/python3 /home/pi/src/yahboom-raspi-cooling-fan/fan_temp.py
@reboot /usr/bin/python3 /home/pi/src/yahboom-raspi-cooling-fan/oled.py
```

See Also
--------

* [dogweather/yahboom-raspi-cooling-fan](https://github.com/dogweather/yahboom-raspi-cooling-fan)
* [YahboomTechnology RGB_Cooling_Hat Official Website](http://www.yahboom.net/study/RGB_Cooling_HAT)
* [YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT](https://github.com/YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT)
* [Adafruit PiOLED - 128x32 Mini OLED for Raspberry Pi](https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage)
* [Shell scripts for system monitoring](https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load)
* [How can I find active network interface from userland?](https://unix.stackexchange.com/questions/347046/how-can-i-find-active-network-interface-from-userland)
