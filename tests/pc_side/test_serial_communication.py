import serial


def send_to_raspberry(message):
    ser = serial.Serial("COM4", 9600)  # replace with the correct serial port for your PC

    ser.write(message.encode())
    ser.close()


send_to_raspberry("Hello world")
