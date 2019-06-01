import pygame
from RemoteRobot import RemoteRobot

# Connect to the EV3s
blueRobot = RemoteRobot('00:17:E9:B2:8A:AF')  # BLUE
yellowRobot = RemoteRobot('00:17:EC:F6:16:26')  # YELLOW

blueRobot.connect()
yellowRobot.connect()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Robot:
    def __init__(self, robot, color, name):
        self.robot = robot
        self.color = color
        self.name = name

robots = [Robot(blueRobot, BLUE, 'BLUE'), Robot(yellowRobot, YELLOW, 'YELLOW')]


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 40)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def button(self, screen, color, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        rect = (self.x, self.y, 200, self.line_height)
        pygame.draw.rect(screen, color, rect)
        screen.blit(textBitmap, [self.x + 10, self.y])
        self.y += self.line_height
        return rect

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 30

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen [width,height]
size = [800, 300]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Soccerbot Host")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while done == False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    mousePos = pygame.mouse.get_pos()
    mouseClick = pygame.mouse.get_pressed()

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.print(screen, "Joystick {}".format(i))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name))

        robot = robots[i]
        connected = robot.robot.is_connected()
        rect = textPrint.button(screen, GREEN if connected else RED, robot.name)
        robot.robot.use_joystick(pygame.joystick.Joystick(i))
        if not connected and rect[0] < mousePos[0] < rect[0] + rect[2] and rect[1] < mousePos[1] < rect[1] + rect[3] and mouseClick[0] == 1:
            robot.robot.connect()

        textPrint.unindent()


    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

# Close the window and quit.

blueRobot.close()
yellowRobot.close()

# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
