# YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT

Working OLED Python Script for **Raspberry Pi OS 64-bit** 

I couldn't get the official or [dogweather](https://github.com/dogweather)'s instructions to work so I did some research and made the necessary corrections.
I'm not an expert with this language or device so this is mostly some basic adjustments/merging of scripts to get the HAT to work.
I also modified the script to be formatted in a manner that I like:
The script is designed to detect and show your active network adapter as part of your device's network details.

## How to run the Python code
**0. Enable I2C**

download RGB_Cooling_Hat.zip from YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT/4.Python programming/RGB_Cooling_HAT.zip (or click [here](https://github.com/YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT/blob/master/4.Python%20programming/RGB_Cooling_HAT.zip))

**1. Enable I2C**

sudo [raspi-config](https://www.raspberrypi.org/documentation/configuration/raspi-config.md) and enable I2C.

**2. Install Python3 Packages**

sudo pip3 install adafruit-circuitpython-ssd1306

**3. Run one or more of the Python scripts**

For example, if you want the Fan, RGB, and OLED all controlled
by temperature and the Pi's stats, then in three separate terminal
windows, run:

```bash
python3 fan_temp.py
```

```bash
python3 rgb_temp.py
```

```bash
python3 oled.py
```

### Starting a script automatically when booting

This easiest way I've found so far is to add a line
to root's crontab with `sudo crontab -e`:

```
@reboot /usr/bin/python3 /home/pi/src/yahboom-raspi-cooling-fan/RGB_Cooling_HAT.py
```

Multiple `@reboot` lines can be given. E.g., I'm currently running these two so that
the lights simply stay default green and aren't changed:

```
@reboot /usr/bin/python3 /home/pi/src/yahboom-raspi-cooling-fan/fan_temp.py
@reboot /usr/bin/python3 /home/pi/src/yahboom-raspi-cooling-fan/oled.py
```

See Also
--------

* [dogweather/yahboom-raspi-cooling-fan](https://github.com/dogweather/yahboom-raspi-cooling-fan)
* [YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT](https://github.com/YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT)
* [Adafruit PiOLED - 128x32 Mini OLED for Raspberry Pi](https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage)
* [Shell scripts for system monitoring](https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load)
* [How can I find active network interface from userland?](https://unix.stackexchange.com/questions/347046/how-can-i-find-active-network-interface-from-userland)
