import pygame
from RemoteRobot import RemoteRobot
from Command import Command
from enum import Enum

# System states
State = Enum('State', ['Start', 'Attract', 'InGame'])
state = State.Start

# Connect to the EV3s
blueRobot = RemoteRobot('00:17:E9:B2:8A:AF')  # BLUE
yellowRobot = RemoteRobot('00:17:EC:F6:16:26')  # YELLOW


def deadzone(val):
    return val if abs(val) > 3 else 0


def use_joystick(joystick):
    left_stick = deadzone(joystick.get_axis(1) * -100)
    right_stick = deadzone(joystick.get_axis(4) * -100)

    hat = joystick.get_hat(0)
    if hat[0] != 0 or hat[1] != 0:
        left_stick = (hat[1] + hat[0]) * 50
        right_stick = (hat[1] - hat[0]) * 50

    buttons = joystick.get_numbuttons()
    pressed = 0
    for i in range(buttons):
        pressed += joystick.get_button(i)

    return Command(left_stick, right_stick, pressed)


pygame.init()

import buttons
import led
import neo
import sounds

##
## Start pygame
neo.startup(0.1) # Startup percent progress

# Set the width and height of the screen [width,height]
size = [1, 1]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Soccerbot Host")

neo.startup(0.5) # Startup percent progress

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

neo.startup(1.0) # Startup percent progress

# -------- Main Program Loop -----------

# Remember the red button state so we can detect long press
lastRedButton = False

# Loop until the user clicks the close button.
done = False

while not done:
    blueRobot.connect()
    yellowRobot.connect()

    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    redButton = buttons.get_red_button()
    greenButton = buttons.get_green_button()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        command = use_joystick(joystick)


    # Limit to 20 frames per second
    clock.tick(20)

# Close the window and quit.

blueRobot.close()
yellowRobot.close()

# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
