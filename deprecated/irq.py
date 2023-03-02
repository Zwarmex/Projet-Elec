"""
This code is used to measure distance using a HC-SR04 ultrasonic sensor, display the distance on two 7-segment displays, and trigger an alarm if the distance is less than 30 cm. It also lights up a dot on the meter if the distance is greater than 100 cm. 

The functions in this code are:

    - format_distance(distance: float) -> str: Formats the distance into a two-digit string
    - handle_echo(pin): Handles the echo signal from the sensor
    - handle_timeout_echo(time): Handles the timeout for the echo signal
    - send_trigger(): Sends a trigger signal to the sensor
    - get_pins(number: int) -> str: Converts a number from 0 to 9 into a string of 0s and 1s for the 7-segment display
    - write_distance(distance: str) -> None: Writes the distance to the 7-segment display

The pins used in this code are:

    - Pin 0: LED alarm
    - Pin 1: LED working
    - Pins 9-15 and 16-22: 7-segment display (left and right)
    - Pin 26: Dot on meter
    - Pin 27: Echo signal from HC-SR04 sensor
    - Pin 28: Trigger signal to HC-SR04 sensor

The global variables used in this code are:

    - timeout_echo: Timer object used to handle timeouts for the echo signal
    - distance_cm: String representing the distance in centimeters
    - bool_running: Boolean used to control the while loop in the main function
"""

from machine import Pin, Timer
import utime

def format_distance(distance: float):
    """
    Formats the distance into a two-digit string

    :param distance: float representing the distance in centimeters
    :return: str representing the dmistance formatted as a two-digit string
    """
    return "%02d" % distance

def handle_echo(pin):
    """
    Handles the echo signal from the HC-SR04 sensor

    :param pin: Pin object representing the echo signal from the sensor
    """
    global timeout_echo
    timeout_echo.deinit()
    timestamp_echo = utime.ticks_us()
    global distance_cm
    distance_cm = format_distance((utime.ticks_diff(timestamp_echo, timestamp_trig)) / 58)
    print(f"diff : {utime.ticks_diff(timestamp_echo, timestamp_trig)} \n \
    dist : {distance_cm} \n \
    trig : {timestamp_trig} \n \
    echo : {timestamp_echo}")

def handle_timeout_echo(time):
    """
    Handles the timeout for the echo signal from the HC-SR04 sensor

    :param time: int representing the time in microseconds
    """
    print("timeout echo :(")

def send_trigger():
    """
    Sends a trigger signal to the HC-SR04 sensor
    """
    global timestamp_trig
    global timeout_echo
    pin_hc_trig.on()
    timestamp_trig = utime.ticks_us()
    utime.sleep_us(10)
    pin_hc_trig.off()
    timeout_echo.init(period=15, mode=Timer.ONE_SHOT, callback=handle_timeout_echo)

def get_pins(number: int) -> str:
    """
    Converts a number from 0 to 9 into a string of 0s and 1s for the 7-segment display

    :param number: int representing the number to be converted
    :return: str representing the state of the pins for the 7-segment display
    """
    pins_state: list = ["1111110", "0110000", "1101101", "1111001", "0110011",
                        "1011011", "1011111", "1110000", "1111111", "1111011"]
    return pins_state[number]

def write_distance(distance: str) -> None:
    """
    Writes the distance to the 7-segment display

    :param distance: str representing the distance to be displayed on the 7-segment display
    """
    state_display_left: str = get_pins(int(distance[0]))
    state_display_right: str = get_pins(int(distance[1]))
    for index in range(len(state_display_left)):
        displays[0][index].value(int(state_display_left[index]))
        displays[1][index].value(int(state_display_right[index]))

pin_led_alarm: Pin = Pin(0, mode=Pin.OUT, value=0)
pin_led_working: Pin = Pin(1, mode=Pin.OUT, value=0)
displays=[[], []] #left, right
for i in range(7):
    displays[0].append(Pin(9 + i, mode=Pin.OUT, value=0))
    displays[1].append(Pin(16 + i, mode=Pin.OUT, value=0))
pin_dot_meter: Pin = Pin(26, mode=Pin.OUT, value=0)
pin_hc_echo: Pin = Pin(27, mode=Pin.IN)
pin_hc_echo.irq(trigger=Pin.IRQ_RISING, handler=handle_echo)
pin_hc_trig: Pin = Pin(28, mode=Pin.OUT, value=0)
bool_running: bool = True
timeout_echo: Timer = Timer()
distance_cm: str = '00'

while bool_running:
    pin_dot_meter.off()
    send_trigger()
    print(f"\033cDistance in CM : {distance_cm} cm.")
    if int(distance_cm) < 30:
        pin_led_working.off()
        print("\nAlarm ! \n")
        pin_led_alarm.toggle()
        utime.sleep_ms(500)
        pin_led_alarm.toggle()
    else:
        pin_led_working.on()
    if int(distance_cm) > 100:
        pin_dot_meter.on()
    write_distance(distance_cm)
    utime.sleep(1)
