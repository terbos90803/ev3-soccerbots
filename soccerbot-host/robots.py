from RemoteRobot import RemoteRobot
import threading
import time

# Connect to the EV3s
blueRobot = RemoteRobot('00:17:E9:B2:8A:AF')  # BLUE
yellowRobot = RemoteRobot('00:17:EC:F6:16:26')  # YELLOW

done = False

def _run_robot(robot):
  while not done:
    robot.connect()
    time.sleep(1)
  robot.close()

_blue_thread = threading.Thread(target=_run_robot, args=(blueRobot,), daemon=True)
_yellow_thread = threading.Thread(target=_run_robot, args = (yellowRobot,), daemon=True)

def start():
  _blue_thread.start()
  _yellow_thread.start()