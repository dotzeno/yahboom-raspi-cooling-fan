import smbus
import time
import os
bus = smbus.SMBus(1)

addr = 0x0d
fan_reg = 0x08
state = 0
temp = 0
level_temp = 0

while True:
    cmd = os.popen('cat /sys/class/thermal/thermal_zone*/temp').readline().strip()
    CPU_TEMP = int(cmd[:2])
    print(CPU_TEMP)
    temp = float(CPU_TEMP)

    if abs(temp - level_temp) >= 1:
        if temp <= 45:
            level_temp = 45
            bus.write_byte_data(addr, fan_reg, 0x00)
        elif temp <= 47:
            level_temp = 47
            bus.write_byte_data(addr, fan_reg, 0x04)
        elif temp <= 49:
            level_temp = 49
            bus.write_byte_data(addr, fan_reg, 0x06)
        elif temp <= 51:
            level_temp = 51
            bus.write_byte_data(addr, fan_reg, 0x08)
        elif temp <= 53:
            level_temp = 53
            bus.write_byte_data(addr, fan_reg, 0x09)
        else:
            level_temp = 55
            bus.write_byte_data(addr, fan_reg, 0x01)

    time.sleep(1)
    
