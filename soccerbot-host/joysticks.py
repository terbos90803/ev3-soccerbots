import pygame
from Command import Command
import neo
import time


commands = [Command(0,0,0), Command(0,0,0)]
ok = [neo.red, neo.red]

_last_commands = commands.copy()
_last_heard = [0.0, 0.0]

def deadzone(val):
  return val if abs(val) > 3 else 0


def get_joystick_command(joystick):
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


def update():
  # Get count of joysticks
  joystick_count = pygame.joystick.get_count()

  # For each joystick:
  for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()

    commands[i] = get_joystick_command(joystick)
    if commands[i] != _last_commands[i]:
      _last_heard[i] = time.monotonic()
      _last_commands[i] = commands[i]
    too_long = time.monotonic() - _last_heard[i] > 60.0
    ok[i] = neo.yellow if too_long else neo.green

