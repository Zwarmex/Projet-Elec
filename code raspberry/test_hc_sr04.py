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
Pin 28 Trigg
"""

from machine import Pin
import time

pin_led_alarm = Pin(0, mode=Pin.OUT, value=0)
pin_led_working = Pin(1, mode=Pin.OUT, value=0)
pin_left_display_a = Pin(9, mode=Pin.OUT, value=0)
pin_left_display_b = Pin(10, mode=Pin.OUT, value=0)
pin_left_display_c = Pin(11, mode=Pin.OUT, value=0)
pin_left_display_d = Pin(12, mode=Pin.OUT, value=0)
pin_left_display_e = Pin(13, mode=Pin.OUT, value=0)
pin_left_display_f = Pin(14, mode=Pin.OUT, value=0)
pin_left_display_g = Pin(15, mode=Pin.OUT, value=0)
pin_right_display_a = Pin(16, mode=Pin.OUT, value=0)
pin_right_display_b = Pin(17, mode=Pin.OUT, value=0)
pin_right_display_c = Pin(18, mode=Pin.OUT, value=0)
pin_right_display_d = Pin(19, mode=Pin.OUT, value=0)
pin_right_display_e = Pin(20, mode=Pin.OUT, value=0)
pin_right_display_f = Pin(21, mode=Pin.OUT, value=0)
pin_right_display_g = Pin(22, mode=Pin.OUT, value=0)
pin_dot_meter = Pin(26, mode=Pin.OUT, value=0)
pin_hc_echo = Pin(27, mode=Pin.IN)
pin_hc_trig = Pin(28, mode=Pin.OUT, value=0)
bool_running = True

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
    distance_cm: str = "{:02d}".format(duration/58)
    return distance_cm

def write_distance(distance: str) -> None:
    if int(distance[0]) == 0:
        pin_left_display_a.value(1)
        pin_left_display_b.value(1)
        pin_left_display_c.value(1)
        pin_left_display_d.value(1)
        pin_left_display_e.value(1)
        pin_left_display_f.value(1)
        pin_left_display_g.value(0)
    elif int(distance[0]) == 1:
        pin_left_display_a.value(0)
        pin_left_display_b.value(1)
        pin_left_display_c.value(1)
        pin_left_display_d.value(0)
        pin_left_display_e.value(0)
        pin_left_display_f.value(0)
        pin_left_display_g.value(0)
    elif int(distance[0]) == 2:
        pin_left_display_a.value(1)
        pin_left_display_b.value(1)
        pin_left_display_c.value(0)
        pin_left_display_d.value(1)
        pin_left_display_e.value(1)
        pin_left_display_f.value(0)
        pin_left_display_g.value(1)
    elif int(distance[0]) == 3:
        pin_left_display_a.value(1)
        pin_left_display_b.value(1)
        pin_left_display_c.value(1)
        pin_left_display_d.value(1)
        pin_left_display_e.value(0)
        pin_left_display_f.value(0)
        pin_left_display_g.value(1)
    elif int(distance[0]) == 4:
        pin_left_display_a.value(0)
        pin_left_display_b.value(1)
        pin_left_display_c.value(1)
        pin_left_display_d.value(0)
        pin_left_display_e.value(0)
        pin_left_display_f.value(1)
        pin_left_display_g.value(1)
    elif int(distance[0]) == 5:
        pin_left_display_a.value(1)
        pin_left_display_b.value(0)
        pin_left_display_c.value(1)
        pin_left_display_d.value(1)
        pin_left_display_e.value(0)
        pin_left_display_f.value(1)
        pin_left_display_g.value(1)
    elif int(distance[0]) == 6:
        pin_left_display_a.value(1)
        pin_left_display_b.value(0)
        pin_left_display_c.value(1)
        pin_left_display_d.value(1)
        pin_left_display_e.value(1)
        pin_left_display_f.value(1)
        pin_left_display_g.value(1)
    elif int(distance[0]) == 7:
        pin_left_display_a.value(1)
        pin_left_display_b.value(1)
        pin_left_display_c.value(1)
        pin_left_display_d.value(0)
        pin_left_display_e.value(0)
        pin_left_display_f.value(0)
        pin_left_display_g.value(0)
    elif int(distance[0]) == 8:
        pin_left_display_a.value(1)
        pin_left_display_b.value(1)
        pin_left_display_c.value(1)
        pin_left_display_d.value(1)
        pin_left_display_e.value(1)
        pin_left_display_f.value(1)
        pin_left_display_g.value(1)
    elif int(distance[0]) == 9:
        pin_left_display_a.value(1)
        pin_left_display_b.value(1)
        pin_left_display_c.value(1)
        pin_left_display_d.value(1)
        pin_left_display_e.value(0)
        pin_left_display_f.value(1)
        pin_left_display_g.value(1)
    if int(distance[1]) == 0:
        pin_right_display_a.value(1)
        pin_right_display_b.value(1)
        pin_right_display_c.value(1)
        pin_right_display_d.value(1)
        pin_right_display_e.value(1)
        pin_right_display_f.value(1)
        pin_right_display_g.value(0)
    elif int(distance[1]) == 1:
        pin_right_display_a.value(0)
        pin_right_display_b.value(1)
        pin_right_display_c.value(1)
        pin_right_display_d.value(0)
        pin_right_display_e.value(0)
        pin_right_display_f.value(0)
        pin_right_display_g.value(0)
    elif int(distance[1]) == 2:
        pin_right_display_a.value(1)
        pin_right_display_b.value(1)
        pin_right_display_c.value(0)
        pin_right_display_d.value(1)
        pin_right_display_e.value(1)
        pin_right_display_f.value(0)
        pin_right_display_g.value(1)
    elif int(distance[1]) == 3:
        pin_right_display_a.value(1)
        pin_right_display_b.value(1)
        pin_right_display_c.value(1)
        pin_right_display_d.value(1)
        pin_right_display_e.value(0)
        pin_right_display_f.value(0)
        pin_right_display_g.value(1)
    elif int(distance[1]) == 4:
        pin_right_display_a.value(0)
        pin_right_display_b.value(1)
        pin_right_display_c.value(1)
        pin_right_display_d.value(0)
        pin_right_display_e.value(0)
        pin_right_display_f.value(1)
        pin_right_display_g.value(1)
    elif int(distance[1]) == 5:
        pin_right_display_a.value(1)
        pin_right_display_b.value(0)
        pin_right_display_c.value(1)
        pin_right_display_d.value(1)
        pin_right_display_e.value(0)
        pin_right_display_f.value(1)
        pin_right_display_g.value(1)
    elif int(distance[1]) == 6:
        pin_right_display_a.value(1)
        pin_right_display_b.value(0)
        pin_right_display_c.value(1)
        pin_right_display_d.value(1)
        pin_right_display_e.value(1)
        pin_right_display_f.value(1)
        pin_right_display_g.value(1)
    elif int(distance[1]) == 7:
        pin_right_display_a.value(1)
        pin_right_display_b.value(1)
        pin_right_display_c.value(1)
        pin_right_display_d.value(0)
        pin_right_display_e.value(0)
        pin_right_display_f.value(0)
        pin_right_display_g.value(0)
    elif int(distance[1]) == 8:
        pin_right_display_a.value(1)
        pin_right_display_b.value(1)
        pin_right_display_c.value(1)
        pin_right_display_d.value(1)
        pin_right_display_e.value(1)
        pin_right_display_f.value(1)
        pin_right_display_g.value(1)
    elif int(distance[1]) == 9:
        pin_right_display_a.value(1)
        pin_right_display_b.value(1)
        pin_right_display_c.value(1)
        pin_right_display_d.value(1)
        pin_right_display_e.value(0)
        pin_right_display_f.value(1)
        pin_right_display_g.value(1)

while bool_running:
    pin_dot_meter.value(0)
    distance_cm: str = measure_distance()
    print(f"\033cDistance in CM : {distance_cm}")
    if int(distance_cm) < 30:
        pin_led_working.value(0)
        print("\nAlarm ! \n")
        pin_led_alarm.value(1)
        time.sleep(0.5)
        pin_led_alarm.value(0)
    else:
        pin_led_working.value(1)
    if int(distance_cm) > 100:
        pin_dot_meter.value(1)
    write_distance(distance_cm)
    time.sleep(1)