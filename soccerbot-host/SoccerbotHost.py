import pygame
from RemoteRobot import RemoteRobot
from Command import Command

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


class RobotDesc:
    def __init__(self, robot, color, name):
        self.robot = robot
        self.color = color
        self.name = name


class Button:
    def __init__(self, rd):
        self.rd = rd
        self.active = False
        self.rect = None


class Selector:
    def __init__(self):
        self.buttons = [Button(blue_rd), Button(yellow_rd)]


blue_rd = RobotDesc(blueRobot, BLUE, 'BLUE')
yellow_rd = RobotDesc(yellowRobot, YELLOW, 'YELLOW')
selectors = [Selector(), Selector()]


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 40)

    def print(self, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def button(self, color, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        rect = (self.x, self.y, textBitmap.get_width() + 20, self.line_height)
        pygame.draw.rect(screen, color, rect)
        screen.blit(textBitmap, [self.x + 10, self.y])
        self.y += self.line_height
        return rect

    def selector(self, sel, command):
        x = self.x
        for b in sel.buttons:
            r = b.rd
            textBitmap = self.font.render(r.name, True, BLACK)
            rect = pygame.Rect(x, self.y, textBitmap.get_width() + 20, self.line_height)
            color = GREEN if b.active and r.robot.is_connected() else RED if b.active else WHITE
            pygame.draw.rect(screen, color, rect)
            screen.blit(textBitmap, [x + 10, self.y])
            b.rect = rect
            if newClick and rect.collidepoint(mousePos):
                b.active = not b.active
                if b.active:
                    r.robot.connect()
            if b.active:
                r.robot.send_command(command)

            x += rect[2]
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 30

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


def deadzone(val):
    return val if abs(val) > 3 else 0


def use_joystick(joystick):
    left_stick = deadzone(joystick.get_axis(1) * -100)
    right_stick = deadzone(joystick.get_axis(3) * -100)

    hat = joystick.get_hat(0)
    if hat[0] != 0 or hat[1] != 0:
        left_stick = (hat[1] + hat[0]) * 50
        right_stick = (hat[1] - hat[0]) * 50

    buttons = joystick.get_numbuttons()
    pressed = 0
    for i in range(buttons):
        pressed += joystick.get_button(i)

    return left_stick, right_stick, pressed


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

last_mouse_press = False

# -------- Main Program Loop -----------
while not done:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    mousePos = pygame.mouse.get_pos()
    mouseClick = pygame.mouse.get_pressed()[0]
    newClick = mouseClick and not last_mouse_press
    last_mouse_press = mouseClick

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.print("Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.print("Joystick {}".format(i))
        textPrint.indent()

        left_stick, right_stick, pressed = use_joystick(joystick)
        joystick_active = left_stick != 0 or right_stick != 0 or pressed != 0

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.button(GREEN if joystick_active else WHITE, "Joystick name: {}".format(name))
        textPrint.indent()

        textPrint.selector(selectors[i], Command(left_stick, right_stick, pressed))

        textPrint.unindent()
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
