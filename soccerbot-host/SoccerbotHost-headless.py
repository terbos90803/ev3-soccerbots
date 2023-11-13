import pygame
from enum import Enum

# System states
State = Enum('State', ['Start', 'Attract', 'Test', 'InGame'])
state = State.Start

# Main Loop Rate
rate = 20 # 20Hz main loop rate

# Enable status lights
import neo
neo.startup(0.1) # Startup percent progress

##
## Start pygame
pygame.init()

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
import joysticks
pygame.joystick.init()

neo.startup(0.5)
# Initialize sounds
import sounds
sounds.init()

neo.startup(0.6)
# Initialize state
left_color = neo.blue
right_color = neo.yellow

neo.startup(0.7)
# Start robot comms
from Command import Command
import robots
robots.start()
robot_enable = False
disable_command = Command(0,0,0)

neo.startup(0.8)
# Start last two hardware drivers
import buttons
import led


neo.startup(1.0) # Startup complete


# -------- Main Program Loop -----------
game_time = 0

# Loop until the user clicks the close button.
done = False
shutdown = False

while not done:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # Hold the red button for 5 seconds to really shut down
    if buttons.red_button_hold_count() > 5 * rate:
        shutdown = True
        done = True

    # Update HID inputs
    buttons.update()
    joysticks.update()

    redButton = buttons.get_red_button()
    greenButton = buttons.get_green_button()

    # Update displays
    neo.set_left_status(left_color, joysticks.ok[0], robots.blueRobot.is_connected())
    neo.set_right_status(right_color, joysticks.ok[1], robots.yellowRobot.is_connected())

    # Game State
    if state == State.Start:
        led.clear()
        # Clear any latent button presses
        buttons.red_button_pressed()
        buttons.green_button_pressed()
        state = State.Attract

    elif state == State.Attract:
        robot_enable = False
        led.show_marquee()
        neo.set_game_status(neo.black)
        if buttons.red_button_pressed():
            state = State.Test
        elif buttons.green_button_pressed():
            game_time = 60
            sounds.play_match_start()
            state = State.InGame

    elif state == State.Test:
        robot_enable = True
        led.show_text('Test')
        neo.set_game_status(neo.yellow)
        if buttons.red_button_pressed() or buttons.green_button_pressed():
            state = State.Start

    elif state == State.InGame:
        robot_enable = True
        led.show_time(game_time)
        game_time -= 1.0/rate
        neo.set_game_status(neo.green)
        if buttons.red_button_pressed():
            sounds.play_match_abort()
            state = State.Start
        elif buttons.green_button_pressed():
            sounds.play_match_win()
            state = State.Start
        elif game_time <= 0:
            sounds.play_match_end()
            state = State.Start

    else: # default - Shouldn't ever get here
        state = State.Start

    # Command robots
    # Must always send some command to keep the link alive
    robots.blueRobot.send_command(joysticks.commands[0] if robot_enable else disable_command)
    robots.yellowRobot.send_command(joysticks.commands[1] if robot_enable else disable_command)
    
    # Limit to 20 frames per second
    clock.tick(rate)

# Close the window and quit.
neo.set_shutdown()
robots.quit()

# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

neo.clear()
led.clear()

if shutdown:
    print('shutting down')
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

