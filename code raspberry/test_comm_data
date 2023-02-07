"""
Pin 0 led red
Pin 1 led green
Pin 26 dot
Pin 27 Echo
Pin 28 Trigg
"""

from machine import Pin
import time
import serial
from dotenv import load_dotenv
import os

load_dotenv()
pin_led_alarm = Pin(0, mode=Pin.OUT, value=0)
pin_led_working = Pin(1, mode=Pin.OUT, value=0)
pin_dot_meter = Pin(26, mode=Pin.OUT, value=0)
pin_hc_echo = Pin(27, mode=Pin.IN)
pin_hc_trig = Pin(28, mode=Pin.OUT, value=0)
serial_port = serial.Serial(os.getenv("NAME_DEVICE"), 9600)  # Open the serial port

def measure_distance() -> int:
    # Start a new measurement :
    pin_hc_trig.value(1)
    time.sleep_us(10)
    pin_hc_trig.value(0)

    # Read the result :
    start = time.ticks_us()
    while not pin_hc_echo.value():
        start = time.ticks_us()
    while pin_hc_echo.value():
        end = time.ticks_us()
    duration = time.ticks_diff(end, start)
    distance_cm: int = int(duration / 58)
    return distance_cm

while True:
    pin_dot_meter.value(0)
    distance_cm: int = measure_distance()
    print(f"\033cDistance in CM : {distance_cm}")
    if distance_cm < 30:
        pin_led_working.value(0)
        print("\nAlarm ! \n")
        pin_led_alarm.value(1)
        time.sleep(0.5)
        pin_led_alarm.value(0)
    else:
        pin_led_working.value(1)
    if distance_cm > 100:
        pin_dot_meter.value(1)
    serial_port.write(distance_cm.encode())  # Write data to the serial port
    time.sleep(1)