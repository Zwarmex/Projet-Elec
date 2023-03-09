"""
Pin 0 led red
Pin 1 led green
Pin 9 A left display
Pin 10 B left display
Pin 11 C left display
Pin 12 D left display
Pin 13 E left display
Pin 14 F left display
Pin 15 G left display
Pin 16 A right display
Pin 17 B right display
Pin 18 C right display
Pin 19 D right display
Pin 20 E right display
Pin 21 F right display
Pin 22 G right display
Pin 26 dot
Pin 27 Echo
Pin 28 Trig
"""


from machine import Pin
import time
import sys


#################INIT################
led=Pin("LED", Pin.OUT, value=0)    #
led(1)                              #
time.sleep(0.5)                     #
led(0)                              #
#####################################
pin_display_dot: Pin = Pin(4, Pin.OUT, value=0)

try:
    while True:
        pin_display_dot.toggle()
        time.sleep(1)
        
            
except KeyboardInterrupt:
    pin_display_dot.off()
