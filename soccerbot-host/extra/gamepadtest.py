from inputs import devices
from inputs import get_gamepad

print(devices)

while True:
	events = get_gamepad()
	for event in events:
		print(event.ev_type, event.code, event.state)
		
