import time
import board
import digitalio

speaker = digitalio.DigitalInOut(board.D17)
speaker.direction = digitalio.Direction.OUTPUT

while True:
	speaker.value = True
	time.sleep(0.001)
	speaker.value = False
	time.sleep(0.001)
