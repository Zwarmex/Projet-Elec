"""
Pin 1 led
Pin 26 dot
Pin 27 Echo
Pin 28 Trigg
"""

from machine import Pin
import time

PIN_TRIG = Pin(28, mode=Pin.OUT)
PIN_ECHO = Pin(27, mode=Pin.IN)
LED = Pin(0, mode=Pin.OUT, value=0)
DOT = Pin(26, mode=Pin.OUT, value=0)

def measure_distance() -> int:
    # Start a new measurement:
    PIN_TRIG.value(1)
    time.sleep_us(10)
    PIN_TRIG.value(0)

    # Read the result:
    start = time.ticks_us()
    while not PIN_ECHO.value():
        start = time.ticks_us()
    while PIN_ECHO.value():
        end = time.ticks_us()
    duration = time.ticks_diff(end, start)
    distance_cm: int = int(duration / 58)
    return distance_cm

while True:
    DOT.value(0)
    distance_cm: int = measure_distance()
    print(f"\033cDistance in CM : {distance_cm}")
    if distance_cm < 30:
        print("\nAlarm ! \n")
        LED.value(1)
        time.sleep(0.5)
        LED.value(0)
    if distance_cm > 100:
        DOT.value(1)
    time.sleep(1)