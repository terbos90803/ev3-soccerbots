import RPi.GPIO as GPIO  
import time

_green_button = 12
_red_button = 26

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(_green_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # set as input (button)  
GPIO.setup(_red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # set as input (button)  

def get_green_button():
  return GPIO.input(_green_button) == 0
  
def get_red_button():
  return GPIO.input(_red_button) == 0

_last_green_button = False
_last_red_button = False
_green_button_pressed = False
_red_button_pressed = False
_green_button_hold = 0
_red_button_hold = 0

def update():
  global _last_green_button, _last_red_button
  global _green_button_pressed, _red_button_pressed
  global _green_button_hold, _red_button_hold

  # Get current button state
  green_button = get_green_button()
  red_button = get_red_button()

  # Test for down-pressed edge, ignoring hold
  if green_button and not _last_green_button:
    _green_button_pressed = True
  if red_button and not _last_red_button:
    _red_button_pressed = True

  # Measure total hold time
  _green_button_hold = _green_button_hold + 1 if green_button else 0
  _red_button_hold = _red_button_hold + 1 if red_button else 0
  
  # Save state
  _last_green_button = green_button
  _last_red_button = red_button

def green_button_pressed():
  global _green_button_pressed
  gbp = _green_button_pressed
  _green_button_pressed = False
  return gbp

def red_button_pressed():
  global _red_button_pressed
  rbp = _red_button_pressed
  _red_button_pressed = False
  return rbp

def green_button_hold_count():
  return _green_button_hold

def red_button_hold_count():
  return _red_button_hold


if __name__ == '__main__':
  import neo
  import led
  try:
    gbp = False
    rbp = False

    while True:            # this will carry on until you hit CTRL+C
      update()
      
      neo.clear()
      if get_green_button():
        neo.set_ok(True)
      elif get_red_button():
        neo.set_ok(False)

      if green_button_pressed():
        gbp = not gbp
      neo.set_left_status(neo.green if gbp else neo.black, False, False)

      if red_button_pressed():
        rbp = not rbp
      neo.set_right_status(neo.red if rbp else neo.black, False, False)

      led._disp_left.print(f'{green_button_hold_count():4}')
      led._disp_right.print(f'{red_button_hold_count():4}')

      time.sleep(0.1)         # wait 0.1 seconds  
    
  finally:                   # this block will run no matter how the try block exits  
      GPIO.cleanup()         # clean up after yourself  
