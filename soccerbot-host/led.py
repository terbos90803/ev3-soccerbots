import board
import busio
import time


from adafruit_ht16k33.segments import Seg7x4

_i2c = busio.I2C(board.SCL, board.SDA)
_disp_left = Seg7x4(_i2c, address=(0x70))
_disp_right = Seg7x4(_i2c, address=(0x71))

_disp_left.brightness = 0.5
_disp_right.brightness = 0.5

_marquee = '    PLAY SoccerBots    '


def clear():
  _disp_left.fill(0)
  _disp_right.fill(0)
  
def show_text(text):
  _disp_left.print(text)
  _disp_right.print(text)
  
def show_time(total_seconds):
  seconds = (int)(total_seconds % 60)
  minutes = (int)(total_seconds / 60)
  min_str = f'{minutes:2d}' if minutes > 0 else '  '
  time_str = f'{min_str}:{seconds:02d}'
  show_text(time_str)

def show_marquee():
  s = (int)((time.monotonic() * 2) % (len(_marquee)-4))
  show_text(_marquee[s:s+4])


if __name__ == '__main__':
  for t in range(200,0,-1):
    show_time(t)
    time.sleep(0.05)
    
  clear()
  while True:
    show_marquee()
    time.sleep(0.05)
