from machine import Pin
import time


pin_trig = Pin(17, Pin.OUT, value=0)
pin_echo = Pin(16, Pin.IN, Pin.PULL_DOWN)
while True:
    pin_trig.on()
    time.sleep_us(2)
    pin_trig.off()
    while pin_echo.value()==0:
        pulse_start = time.ticks_us()
    while pin_echo.value()==1:
        pulse_end = time.ticks_us()
    pulse_duration = pulse_end - pulse_start
    distance = round(pulse_duration * 17165 / 1000000, 0)
    print ('Distance:',"{:.0f}".format(distance),'cm')
    time.sleep(1)