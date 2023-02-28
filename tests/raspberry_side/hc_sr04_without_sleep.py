from machine import Pin
import time

number = 0

def handle_echo(pin: Pin) -> None:
    global pulse_start
    global echo_received
    global pulse_end
    pulse_end = time.ticks_us()
    echo_received = True

def handle_trigger(pin: Pin) -> None:
    global pulse_start
    pulse_start = time.ticks_us()

def write_distance(distance):
    global number
    print('n°{} | Distance: {:.0f} cm'.format(number, distance))
    number += 1

def calculate_distance(pulse_duration):
    return round((pulse_duration * 17165 / 1000000) - 40, 0)

def check_distance(distance):
    # global alarmed
    return distance < 30
    # if distance < 30:
    #     alarmed = True
    # alarmed = False

def send_trigger(pin):
    pin.on()
    time.sleep_us(100)
    pin.off()

pin_led_red = Pin(0, Pin.OUT, value=0)
pin_led_green = Pin(1, Pin.OUT, value=0)
pin_echo = Pin(16, Pin.IN, Pin.PULL_DOWN)
pin_echo.irq(handle_echo, Pin.IRQ_FALLING)
pin_trigger = Pin(17, Pin.OUT, value=0)
pin_trigger.irq(handle_trigger, Pin.IRQ_RISING)
alarmed = False
pulse_start = 0
pulse_end = 0
echo_received = False
next_send_trigger = 0
next_toggle_led_red = 0

try:
    while True:
        current_timestamp = time.ticks_us()
        
        # Time to send another trigger
        if time.ticks_diff(current_timestamp, next_send_trigger) >= 0:
            # print("sending")
            send_trigger(pin_trigger)
            next_send_trigger = time.ticks_us() + 1000000
        
        # When echo is received
        if echo_received:
            distance_cm = calculate_distance(pulse_end - pulse_start)
            write_distance(distance_cm)
            alarmed = check_distance(distance_cm)
            echo_received = False
        
        # When the object is nearer than the limit
        if alarmed:
            pin_led_green.off()
            if time.ticks_diff(current_timestamp, next_toggle_led_red) >= 0:
                next_toggle_led_red = time.ticks_us() + 500000
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
