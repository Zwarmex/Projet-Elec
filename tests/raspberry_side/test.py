import sys
import machine
import time
import re

led = machine.Pin("LED", machine.Pin.OUT)
led(1)
time.sleep(0.5)
led(0)

def led_on():
    led(1)

def led_off():
    led(0)


while True:
    # read a command from the host
    reading = sys.stdin.readline().strip()
    # perform the requested action
    line = reading.lower()
    if re.search("led=", line):
        led_value = re.sub("[^0-9]", "", line)
        if led_value:
            led_on()
        else:
            led_off()
        sys.stdout.write(f"{bool(led_value)}\n")