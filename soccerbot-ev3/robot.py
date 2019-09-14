#!/usr/bin/env python3
"""
SSCI SoccerBot robot
"""

import sys
import subprocess
import bluetooth
from Command import Command
from ev3dev2 import DeviceNotFound
from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.led import Led, Leds
from ev3dev2.display import Display
from Screen import init_console, reset_console, debug_print


init_console()

# get handles for the three motors
try:
    rightMotor = LargeMotor(OUTPUT_B)
    leftMotor = LargeMotor(OUTPUT_C)
except DeviceNotFound as error:
    print("Motor not connected")
    print("Check and restart")
    print(error)
    while True:
        pass

leds = Leds()
#debug_print(Led().triggers)
leds.set('LEFT', trigger='default-on')
leds.set('RIGHT', trigger='default-on')

display = Display()
screenw = display.xres
screenh = display.yres

# hostMACAddress = '00:17:E9:B2:8A:AF' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
# Fetch BT MAC address automatically
cmd = "hciconfig"
device_id = "hci0"
sp_result = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
hostMACAddress = sp_result.stdout.split("{}:".format(device_id))[1].split("BD Address: ")[1].split(" ")[0].strip()
debug_print (hostMACAddress)
print (hostMACAddress)

kick_power = 0
max_kick = 1000
max_power = 100
drive_pct = 0.60

port = 3  # port number is arbitrary, but must match between server and client
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
while True:
    try:
        reset_console()
        print (hostMACAddress)
        leds.set_color('LEFT', 'AMBER')
        leds.set_color('RIGHT', 'AMBER')

        client, clientInfo = s.accept()
        print ('Connected')
        leds.set_color('LEFT', 'GREEN')
        leds.set_color('RIGHT', 'GREEN')

        while True:
            data = client.recv(size)
            if data:
                #print(data, file=sys.stderr)
                cmd = Command.unpickled(data)

                if cmd:
                    left_speed=cmd.left_drive * drive_pct
                    right_speed=cmd.right_drive * drive_pct
                    do_kick = cmd.do_kick > 0
                    if do_kick:
                        kick_power = kick_power - (5 if kick_power > 0 else 0)
                        if kick_power > 0:
                            left_speed=max_power
                            right_speed=max_power
                    else:
                        kick_power = kick_power + (1 if kick_power < screenh else 0)

                    leftMotor.on(speed=left_speed)
                    rightMotor.on(speed=right_speed)

                    display.rectangle(x1=0, y1=0, x2=screenw, y2=kick_power)
                    display.update()

    except:
        #print("Closing socket")
        client.close()
s.close()
