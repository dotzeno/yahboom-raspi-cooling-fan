# YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT for 64-bit

Following the [Official Website's](http://www.yahboom.net/study/RGB_Cooling_HAT) Python Installation instructions, I got as far as getting the RGB and Fan working on my RaspberryPi 4B. But I couldn't figure out how to get the OLED working, with just the official instructions. 

I did a little digging and found [dogweather/yahboom-raspi-cooling-fan](https://github.com/dogweather/yahboom-raspi-cooling-fan) but I still couldn't get the OLED to work, so I did some research and made the necessary adjustments to get things working on 64-bit Raspbian OS.

I've adjusted the formatting to my liking and created a function in the script so that it can detect and show, in addition to the IP address, whether or not there's an active network adapter (and what that is) on the OLED display.

Here's how I did it (and hopefully it'll help you too).

### Instructions for use with Raspberry Pi OS 64-bit
Instructions tested with a fresh RaspberryPi 4B with Raspbian OS 64-bit.

**1. Enable I2C**

`sudo raspi-config` and enable I2C. 

You may also enable VNC at this time if that is something you're more comfortable with (i.e. use VNC to remote into the device and use Chromium to download files onto the device).

**2. Install Python3 Packages**

```bash
sudo pip3 install adafruit-circuitpython-ssd1306 --break-system-packages
```
*The system will prompt you to tell you that `--break-system-packages` is bad. I don't know a better way to do this so, proceed!

**3. Download Scripts to Device and Extract**

Download 'RGB_Cooling_Hat_x64.zip' from my [Releases](https://github.com/dotzeno/yahboom-raspi-cooling-fan/releases/download/v0.1/RGB_Cooling_HAT_x64.zip) and extract to the destination directory of your choice.

**4. Run one or more of the Python scripts**

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

### Load script at boot

The easiest way to do this is to `sudo crontab -e`, pick a text editor you're familiar with and then add the following line to crontab:

```
@reboot /usr/bin/python3 /home/pi/RGB_Cooling_HAT_x64/RGB_Cooling_HAT.py
```

If you want to do like dogweather (run two scripts on boot for controlling the fan and OLED; no script to control RGB - RGB will default to ON and GREEN), you can also use Multiple `@reboot` lines, like so (add the following lines to crontab):

```
@reboot /usr/bin/python3 /home/pi/RGB_Cooling_HAT_x64/fan_temp.py
@reboot /usr/bin/python3 /home/pi/RGB_Cooling_HAT_x64/oled.py
```
You may need to correct the target destination to wherever you extracted RGB_Cooling_Hat_x64.zip. For me, that looks like:

```
@reboot /usr/bin/python3 /home/pi/Downloads/RGB_Cooling_HAT_x64/RGB_Cooling_HAT.py
```


See Also
--------

* [The Official raspi-config Documentation](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)
* [dogweather's yahboom-raspi-cooling-fan github repository](https://github.com/dogweather/yahboom-raspi-cooling-fan)
* [YahboomTechnology RGB_Cooling_Hat Official Website](http://www.yahboom.net/study/RGB_Cooling_HAT)
* [YahboomTechnology's Raspberry-Pi-RGB-Cooling-HAT github respository](https://github.com/YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT)
* [Adafruit PiOLED - 128x32 Mini OLED for Raspberry Pi Usage Documentation](https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage)
* [Shell scripts for system monitoring](https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load)
* [How can I find active network interface from userland?](https://unix.stackexchange.com/questions/347046/how-can-i-find-active-network-interface-from-userland)
