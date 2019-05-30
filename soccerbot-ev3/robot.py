#!/usr/bin/env python3
"""
SSCI SoccerBot robot server
"""

import sys
import subprocess
import bluetooth
from Command import Command
from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.led import Leds
from Screen import init_console, debug_print


init_console()

# get handles for the three motors
kickMotor = MediumMotor(OUTPUT_A)
rightMotor = LargeMotor(OUTPUT_B)
leftMotor = LargeMotor(OUTPUT_C)

# reset the kick motor to a known good position
kickMotor.on_for_seconds(speed=-10, seconds=0.5)
kickMotor.on_for_seconds(speed=10, seconds=2, brake=False)
kickMotor.reset()
kicking = False

# hostMACAddress = '00:17:E9:B2:8A:AF' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
# Fetch BT MAC address automatically
cmd = "hciconfig"
device_id = "hci0"
sp_result = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
# print(sp_result.stdout, file=sys.stderr)
hostMACAddress = sp_result.stdout.split("{}:".format(device_id))[1].split("BD Address: ")[1].split(" ")[0].strip()
debug_print (hostMACAddress)
print (hostMACAddress)

port = 3  # port number is arbitrary, but must match between server and client
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
try:
    client, clientInfo = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            #print(data, file=sys.stderr)
            cmd = Command.unpickled(data)

            if cmd:
                leftMotor.on(speed=cmd.left_drive)
                rightMotor.on(speed=cmd.right_drive)
                do_kick = cmd.do_kick > 0
                if do_kick != kicking:
                    kicking = do_kick
                    if do_kick:
                        kickMotor.run_to_abs_pos(position_sp=-90, speed_sp=1000, stop_action="hold")
                    else:
                        kickMotor.run_to_abs_pos(position_sp=0, speed_sp=200, stop_action="hold")

except:
    print("Closing socket")
    client.close()
    s.close()
