import serial

# open a serial connection
serial_com = serial.Serial("COM4", 115200, timeout=0)

# blink the led
while True:
    # string = input("string : ")
    # serial_com.write(f"{string}\n".encode())
    if distance := serial_com.readline().decode():
        print(f"{distance}")