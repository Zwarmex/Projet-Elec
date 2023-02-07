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

pin_led_alarm: Pin = Pin(0, mode=Pin.OUT, value=0)
pin_led_working: Pin = Pin(1, mode=Pin.OUT, value=0)
pins_display_left: list = []
pins_display_right: list = []
for i in range(7):
    pin: Pin = Pin(9 + i, mode=Pin.OUT, value=0)
    pins_display_left.append(pin)
for i in range(7):
    pin: Pin = Pin(16 + i, mode=Pin.OUT, value=0)
    pins_display_right.append(pin)
pin_dot_meter: Pin = Pin(26, mode=Pin.OUT, value=0)
pin_hc_echo: Pin = Pin(27, mode=Pin.IN)
pin_hc_trig: Pin = Pin(28, mode=Pin.OUT, value=0)
bool_running: bool = True


def measure_distance() -> str:
    """
    The function send a start ping to the hc and calculate the distance when the sound come back.
    :return: the distance calculated
    """
    # Start a new measurement :
    end = 0
    pin_hc_trig.value(1)
    time.sleep_us(10)
    pin_hc_trig.value(0)

    # Read the result :
    start = time.ticks_us()
    while not pin_hc_echo.value():
        start = time.ticks_us()
    while pin_hc_echo.value():
        end = time.ticks_us()
    duration: int = time.ticks_diff(end, start)
    distance: str = "%02d" % int(duration / 58)
    return distance


def get_pins(number: int) -> str:
    """
    Gets a number from 0 to 9 and return a string of 0 and 1 for the pins
    :param number: the number to be transformed into 0 and 1
    """
    pins_state: list = ["1111110", "0110000", "1101101", "1111001", "0110011",
                        "1011011", "1011111", "1110000", "1111111", "1111011"]
    return pins_state[number]


def write_distance(distance: str) -> None:
    """
    Change the state of the pins to light some leds or not
    :param distance: write the two firsts numbers
    """
    state_display_left: str = get_pins(int(distance[0]))
    state_display_right: str = get_pins(int(distance[1]))
    for index in range(len(state_display_left)):
        pins_display_left[index].value(int(state_display_left[index]))
    for index in range(len(state_display_right)):
        pins_display_right[index].value(int(state_display_right[index]))


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
