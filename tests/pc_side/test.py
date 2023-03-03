import serial
import time

# open a serial connection
serial_com = serial.Serial("COM4", 115200, timeout=0)

# blink the led
while True:
    string = input("string : ")
    serial_com.write(f"{string}\n".encode())
    
    print(serial_com.readline().strip())
    # time.sleep(1)
    # serial_com.write(b"led0\n")
    # print(serial_com.readline().strip())
    # time.sleep(1)§