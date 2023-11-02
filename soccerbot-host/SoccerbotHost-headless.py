import pygame
from enum import Enum

# System states
State = Enum('State', ['Start', 'Attract', 'InGame'])
state = State.Start


pygame.init()

import buttons
import joysticks
import led
import neo
import robots
import sounds

##
## Start pygame
neo.startup(0.1) # Startup percent progress

# Set the width and height of the screen [width,height]
size = [100, 100]
screen = pygame.display.set_mode(size)

neo.startup(0.2)
pygame.display.set_caption("Soccerbot Host")

neo.startup(0.3)
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

neo.startup(0.4)
# Initialize the joysticks
pygame.joystick.init()

neo.startup(0.5)
# Initialize sounds
sounds.init()

neo.startup(0.6)
# Initialize state
left_color = neo.blue
right_color = neo.yellow

neo.startup(0.7)
# Start robots
robots.start()

neo.startup(1.0) # Startup complete


# -------- Main Program Loop -----------

# Loop until the user clicks the close button.
done = False

while not done:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    buttons.update()
    joysticks.update()

    redButton = buttons.get_red_button()
    greenButton = buttons.get_green_button()

    # Update displays
    neo.set_left_status(left_color, joysticks.ok[0], robots.blueRobot.is_connected())
    neo.set_right_status(right_color, joysticks.ok[1], robots.yellowRobot.is_connected())

    # Command robots
    robots.blueRobot.send_command(joysticks.commands[0])
    robots.yellowRobot.send_command(joysticks.commands[1])
    
    # Limit to 20 frames per second
    clock.tick(20)

# Close the window and quit.
robots.done = True

# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

neo.clear()
