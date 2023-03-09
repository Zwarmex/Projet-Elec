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

def handle_echo(pin: Pin) -> None:
    if pin.value():
        global pulse_start
        pulse_start = time.ticks_us()
    else:
        global pulse_end
        global echo_received
        pulse_end = time.ticks_us()
        echo_received = True

def write_distance(distance: str, displays_array: list) -> None:
    state_display_left: str = get_pins(int(distance[0]))
    state_display_right: str = get_pins(int(distance[1]))
    for index in range(len(displays_array[0])):
        displays_array[0][index].value(int(state_display_left[index]))
    for index in range(len(displays_array[1])):
        displays_array[1][index].value(int(state_display_right[index]))
    print(f'{distance}')
    
def get_pins(number: int) -> str:
    pins_state: list = ["1111101", "0110000", "1101110", "1111010", "0110011",
                        "1011011", "1011111", "1110000", "1111111", "1111011"]
    return pins_state[number]

def calculate_distance(pulse_start: int, pulse_end: int) -> str:
    return "%02d" % (round(time.ticks_diff(pulse_end, pulse_start) / 58, 0))

def check_alarm_and_meters(distance: str, alarm: int) -> bool:
    return int(distance) < alarm, int(distance) >= 100

def send_trigger(pin: Pin) -> None:
    pin.on()
    time.sleep_us(10)
    pin.off()

#################INIT################
led=Pin("LED", Pin.OUT, value=0)    #
led(1)                              #
time.sleep(0.5)                     #
led(0)                              #
#####################################
pin_led_red: Pin = Pin(0, Pin.OUT, value=0)
pin_led_green: Pin = Pin(1, Pin.OUT, value=0)
displays: list= [[],[]] # left, right
for i in range(7):
    displays[0].append(Pin(9+i, Pin.OUT, value=0))
for i in range(7):
    displays[1].append(Pin(16+i, Pin.OUT, value=0))
pin_display_dot: Pin = Pin(26, Pin.OUT, value=0)
pin_echo: Pin = Pin(27, Pin.IN, Pin.PULL_DOWN)
pin_echo.irq(handle_echo, Pin.IRQ_FALLING | Pin.IRQ_RISING)
pin_trigger: Pin = Pin(28, Pin.OUT, value=0)
pulse_start: int = 0
pulse_end: int = 0
next_send_trigger: int = 0
next_toggle_led_red: int = 0
next_timeout_echo: int = 0
alarm_limit: int = 30
echo_received: bool = False
timeout_echo: bool = False
alarmed: bool = False
meters: bool = False


try:
    while True:
        current_timestamp: int = time.ticks_us()
        
        # # read a command from the host
        # reading = sys.stdin.readline().strip()
        # # perform the requested action
        # line = reading.lower()
        # if "led=" in line:
        #     led_value = line.split("=")[1]
            
        # Time to send another trigger
        if current_timestamp >= next_send_trigger :
            # print("sending")
            send_trigger(pin_trigger)
            next_send_trigger: int = time.ticks_us() + 1000000
            next_timeout_echo: int = time.ticks_us() + 60000 # time max travelled by sound for 800cm (400*2)
            timeout_echo: bool = False
        
        # When the echo is in timeout
        if current_timestamp >= next_timeout_echo:
            timeout_echo: bool = True
        
        # When echo is received
        if echo_received:
            if not timeout_echo:
                distance_cm: float = calculate_distance(pulse_start, pulse_end)
                write_distance(distance_cm, displays)
                alarmed, meters = check_alarm_and_meters(distance_cm, alarm_limit)
            else:
                print('Timeout')
                timeout_echo: bool = False
                alarmed: bool = True
            echo_received: bool = False
        
        # When the object is nearer than the limit
        if alarmed:
            pin_display_dot.off()
            pin_led_green.off()
            if current_timestamp >= next_toggle_led_red:
                next_toggle_led_red: int = time.ticks_us() + 500000
                pin_led_red.toggle()
        else:
            if meters:
                pin_display_dot.on()
            else:
                pin_display_dot.off()
            pin_led_red.off()
            pin_led_green.on()        
        
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
