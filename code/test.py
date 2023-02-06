from machine import Pin
import time

alarmed: int = 1
running: int = 1
pin_led = Pin(0, mode=Pin.OUT, value=0)

while running:
    if alarmed:
        pin_led.value(1)
        print("Alarmed")
        time.sleep(0.5)
        pin_led.value(0)
        time.sleep(0.5)

print("EOP")