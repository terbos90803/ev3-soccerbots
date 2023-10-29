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


if __name__ == '__main__':
  import neo
  try:  
    while True:            # this will carry on until you hit CTRL+C  
      if get_green_button():
        neo.set_ok(True)
      elif get_red_button():
        neo.set_ok(False)
      else:
        neo.clear()
      time.sleep(0.1)         # wait 0.1 seconds  
    
  finally:                   # this block will run no matter how the try block exits  
      GPIO.cleanup()         # clean up after yourself  
