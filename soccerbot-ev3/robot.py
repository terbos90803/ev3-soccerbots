#!/usr/bin/env python3
"""
SSCI SoccerBot robot server
"""

import remote
import time

from Command import Command
from ev3dev2 import DeviceNotFound
from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.led import Led, Leds
from ev3dev2.display import Display
from Screen import init_console, reset_console, debug_print


init_console()

# get handles for the three motors
kickMotor = None
rightMotor = None
leftMotor = None
while True:
    try:
        kickMotor = kickMotor if kickMotor else MediumMotor(OUTPUT_A)
        rightMotor = rightMotor if rightMotor else LargeMotor(OUTPUT_B)
        leftMotor = leftMotor if leftMotor else LargeMotor(OUTPUT_C)
        break
    except DeviceNotFound as error:
        print("Motor not connected")
        print("Check and restart")
        print(error)
        time.sleep(1)

leds = Leds()
#debug_print(Led().triggers)
leds.set('LEFT', trigger='default-on')
leds.set('RIGHT', trigger='default-on')

display = Display()
screenw = display.xres
screenh = display.yres

# Create connection to server
s, host_address = remote.get_listener_socket()
s.settimeout(5)

# reset the kick motor to a known good position
kickMotor.on_for_seconds(speed=-10, seconds=0.5)
kickMotor.on_for_seconds(speed=10, seconds=2, brake=False)
kickMotor.reset()
kicking = False
kick_power = 0
max_kick = 1000

# Main loop handles connections to the host
while True:
    try:
        reset_console()
        print (host_address)
        leds.set_color('LEFT', 'AMBER')
        leds.set_color('RIGHT', 'AMBER')
        debug_print('Waiting for connection')
        remote.advertise()

        try:
            client, clientInfo = s.accept()
        except:
            continue

        client.settimeout(10)
        print ('Connected')
        debug_print('Connected to:', clientInfo)
        leds.set_color('LEFT', 'GREEN')
        leds.set_color('RIGHT', 'GREEN')

        # Driving loop
        while True:
            data = client.recv(remote.size)
            #debug_print('recv:', data)
            if data == b'':
                client.close()
                break

            if data:
                #print(data, file=sys.stderr)
                cmd = Command.unpickled(data)
                if cmd == 'ping':
                    continue

                if cmd:
                    leftMotor.on(speed=cmd.left_drive)
                    rightMotor.on(speed=cmd.right_drive)
                    do_kick = cmd.do_kick > 0
                    if do_kick != kicking:
                        kicking = do_kick
                        if do_kick:
                            kickMotor.run_to_abs_pos(position_sp=-100, speed_sp=kick_power*max_kick//screenh, stop_action="hold")
                            kick_power = kick_power - (25 if kick_power > 25 else kick_power)
                        else:
                            kickMotor.run_to_abs_pos(position_sp=-10, speed_sp=200, stop_action="coast")

                    kick_power = kick_power + (1 if kick_power < screenh else 0)
                    display.rectangle(x1=0, y1=0, x2=screenw, y2=kick_power)
                    display.update()

    except:
        #print("Closing socket")
        client.close()
s.close()
