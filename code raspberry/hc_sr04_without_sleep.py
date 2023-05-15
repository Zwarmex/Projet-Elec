"""
Pin 0 led red
Pin 1 led green
Pin 4 dot
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
Pin 27 Echo
Pin 28 Trig
"""

from machine import Pin
import time
import sys
import math
import select


def handle_echo(pin: Pin) -> None:
    if pin.value():
        global pulse_start
        pulse_start = time.ticks_us()
    else:
        global pulse_end
        global waiting_for_echo
        pulse_end = time.ticks_us()
        waiting_for_echo = True


def write_distance(distance: str, displays_array: list) -> None:
    state_display_left: str = get_pins(int(distance[0]))
    state_display_right: str = get_pins(int(distance[1]))
    for index in range(len(displays_array[0])):
        displays_array[0][index].value(int(state_display_left[index]))
    for index in range(len(displays_array[1])):
        displays_array[1][index].value(int(state_display_right[index]))
    print(f"{distance}")


def write_timeout(displays_array: list) -> None:
    pins_timeout: list = ["0001110", "0011101"]
    for indexDisplay in range(len(displays_array)):
        for indexPin in range(len(displays_array[indexDisplay])):
            displays_array[indexDisplay][indexPin].value(
                int(pins_timeout[indexDisplay][indexPin])
            )

    print("00")


def get_pins(number: int) -> str:
    pins_state: list = [
        "1111110",
        "0110000",
        "1101101",
        "1111001",
        "0110011",
        "1011011",
        "1011111",
        "1110000",
        "1111111",
        "1111011",
    ]
    return pins_state[number]


def calculate_distance(pulse_start: int, pulse_end: int) -> str:
    return "%02d" % (round(time.ticks_diff(pulse_end, pulse_start) / 58, 0))


def check_alarm_and_meters(distance: str, alarm: int) -> bool:
    return int(distance) < alarm, int(distance) >= 100


def send_trigger(pin: Pin) -> None:
    pin.on()
    time.sleep_us(10)
    pin.off()


def handle_received_command(command: str) -> None:
    if "alarm=" in command:
        new_alarm_limit = int(command.split("=")[1])
        global alarm_limit
        alarm_limit = new_alarm_limit
        print(f"New alarm limit set to {alarm_limit}")


#################INIT################
led = Pin("LED", Pin.OUT, value=0)  #
led(1)  #
time.sleep(0.5)  #
led(0)  #
#####################################
pin_led_red: Pin = Pin(0, Pin.OUT, value=0)
pin_led_green: Pin = Pin(1, Pin.OUT, value=0)
pin_display_dot: Pin = Pin(2, Pin.OUT, value=0)
displays: list = [[], []]  # left, right
for i in range(7):
    displays[0].append(Pin(9 + i, Pin.OUT, value=0))
for i in range(7):
    displays[1].append(Pin(16 + i, Pin.OUT, value=0))
pin_echo: Pin = Pin(27, Pin.IN, Pin.PULL_DOWN)
pin_echo.irq(handle_echo, Pin.IRQ_FALLING | Pin.IRQ_RISING)
pin_trigger: Pin = Pin(28, Pin.OUT, value=0)
pulse_start: int = 0
pulse_end: int = 0
next_send_trigger: int = 0
next_toggle_led_red: int = 0
next_timeout_echo: int = 0
alarm_limit: int = 30
waiting_for_echo: bool = False
timeout_echo: bool = False
alarmed: bool = False
meters: bool = False

try:
    while True:
        current_timestamp: int = time.ticks_us()

        # Check if there's data to be read from the PC
        if pin_trigger.value() == 0 and select.select([sys.stdin], [], [], 0)[0]:
            received_data = sys.stdin.buffer.readline().strip()
            if received_data:
                received_command = received_data.decode().lower()
                handle_received_command(received_command)

        # Time to send another trigger
        if current_timestamp >= next_send_trigger:
            send_trigger(pin_trigger)
            next_send_trigger: int = time.ticks_us() + 1_000_000
            next_timeout_echo: int = (
                time.ticks_us() + 100_000
            )  # time max travelled by sound for 800cm (400*2)
            timeout_echo: bool = False

        # When the echo is in timeout
        if current_timestamp >= next_timeout_echo and not timeout_echo:
            timeout_echo: bool = True
            alarmed: bool = True
            write_timeout(displays)
            pin_led_red.on()
            pin_led_green.off()
            pin_display_dot.off()

        if current_timestamp >= next_toggle_led_red:
            next_toggle_led_red: int = time.ticks_us() + 500000
            pin_led_red.toggle()

        # When echo is received
        if waiting_for_echo and not timeout_echo:
            distance_cm: float = calculate_distance(pulse_start, pulse_end)
            write_distance(distance_cm, displays)
            alarmed, meters = check_alarm_and_meters(distance_cm, alarm_limit)
            waiting_for_echo: bool = False
            next_timeout_echo = math.inf
            # When the object is nearer than the limit
            if alarmed:
                next_toggle_led_red = current_timestamp
                pin_display_dot.off()
                pin_led_green.off()
            else:
                next_toggle_led_red = math.inf
                if meters:
                    pin_display_dot.on()
                else:
                    pin_display_dot.off()
                pin_led_red.off()
                pin_led_green.on()

# End Of Program
except KeyboardInterrupt:
    pin_led_red.off()
    pin_led_green.off()
    for display in displays:
        for pin in display:
            pin.off()
    pin_display_dot.off()
    pin_echo.off()
    pin_trigger.off()
    print("EOP")
