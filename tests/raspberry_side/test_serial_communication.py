import serial

ser = serial.Serial("/dev/ttyACM0", 9600) # replace with the correct serial port for your Raspberry Pi

while True:
    message = ser.readline().decode()
    print(message)
