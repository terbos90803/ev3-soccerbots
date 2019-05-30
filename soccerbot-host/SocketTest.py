"""
A simple Python script to send messages to a server over Bluetooth using
PyBluez.
"""

import bluetooth

serverMACAddress = '00:17:E9:B2:8A:AF'
port = 3
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress,port))
while 1:
    text = input()
    if text == "quit":
        break
    s.send(bytes(text, 'UTF-8'))
s.close()
