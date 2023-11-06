import time
import board
import neopixel

_pixels = neopixel.NeoPixel(board.D10, 8, brightness=0.1, auto_write=True, pixel_order=neopixel.GRB)

black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)


def clear():
  _pixels.fill(black)
  

def startup(percent):
  clear()
  for ix in range((int)(_pixels.n * percent + 0.5)):
    _pixels[ix] = white


def set_ok(is_ok):
  _pixels[3] = _pixels[4] = green if is_ok else red


def set_system_status(color):
  if _pixels[3] is not color:
    _pixels[3] = _pixels[4] = color


def set_left_status(color, gamepad, robot):
  _pixels[0] = color
  _pixels[1] = green if gamepad else red
  _pixels[2] = green if robot else red
  
  
def set_right_status(color, gamepad, robot):
  _pixels[7] = color
  _pixels[6] = green if gamepad else red
  _pixels[5] = green if robot else red
  
  
if __name__ == '__main__':
  while True:
    print("red")
    for ix in range(8):
      _pixels[ix] = (128,0,0)
      time.sleep(1)
    _pixels.fill(red)
    time.sleep(1)
    
    print("green")
    for ix in range(8):
      _pixels[ix] = (0,128,0)
      time.sleep(1)
    _pixels.fill(green)
    time.sleep(1)
    
    print("blue")
    for ix in range(8):
      _pixels[ix] = (0,0,128)
      time.sleep(1)
    _pixels.fill(blue)
    time.sleep(1)
