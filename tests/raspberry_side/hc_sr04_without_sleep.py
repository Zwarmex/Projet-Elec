from machine import Pin
import time


def handle_echo(pin: Pin) -> None:
    global pulse_start
    global echo_received
    global pulse_end
    pulse_end: int = time.ticks_us()
    echo_received: bool = True

def handle_trigger(pin: Pin) -> None:
    global pulse_start
    pulse_start: int = time.ticks_us()

def write_distance(distance: float) -> None:
    global number_of_trigger
    print('n°{} | Distance: {:.0f} cm'.format(number_of_trigger, distance))
    number_of_trigger += 1

def calculate_distance(pulse_duration: int) -> float:
    return round((pulse_duration * 17165 / 1000000) - 40, 0)

def check_distance(distance: float) -> bool:
    # global alarmed
    return distance < 30
    # if distance < 30:
    #     alarmed = True
    # alarmed = False

def send_trigger(pin: Pin) -> None:
    pin.on()
    time.sleep_us(100)
    pin.off()

pin_led_red: Pin = Pin(0, Pin.OUT, value=0)
pin_led_green: Pin = Pin(1, Pin.OUT, value=0)
pin_echo: Pin = Pin(16, Pin.IN, Pin.PULL_DOWN)
pin_echo.irq(handle_echo, Pin.IRQ_FALLING)
pin_trigger: Pin = Pin(17, Pin.OUT, value=0)
pin_trigger.irq(handle_trigger, Pin.IRQ_RISING)
pulse_start: int = 0
pulse_end: int = 0
number_of_trigger: int = 0
next_send_trigger: int = 0
next_toggle_led_red: int = 0
echo_received: bool = False
alarmed: bool = False


try:
    while True:
        current_timestamp: int = time.ticks_us()
        
        # Time to send another trigger
        if time.ticks_diff(current_timestamp, next_send_trigger) >= 0:
            # print("sending")
            send_trigger(pin_trigger)
            next_send_trigger: int = time.ticks_us() + 1000000
        
        # When echo is received
        if echo_received:
            distance_cm: float = calculate_distance(pulse_end - pulse_start)
            write_distance(distance_cm)
            alarmed: float = check_distance(distance_cm)
            echo_received: bool = False
        
        # When the object is nearer than the limit
        if alarmed:
            pin_led_green.off()
            if time.ticks_diff(current_timestamp, next_toggle_led_red) >= 0:
                next_toggle_led_red: int = time.ticks_us() + 500000
                pin_led_red.toggle()
        else:
            pin_led_red.off()
            pin_led_green.on()

except KeyboardInterrupt:
    pin_led_red.off()
    pin_led_green.off()
    pin_echo.off()
    pin_trigger.off()
    print("EOP")
