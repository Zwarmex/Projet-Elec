import serial
from dotenv import load_dotenv
import os

load_dotenv()

serial_port = serial.Serial(os.getenv("NAME_DEVICE"), 9600)  # Open the serial port
while True:
    data = serial_port.readline().decode()  # Read data from the serial port
    print(data)  # Print the received data
