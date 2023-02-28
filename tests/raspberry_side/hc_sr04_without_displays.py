from machine import Pin, Timer
import time


def handle_echo(pin):
    global pulse_start, echo_timeout, echo_late, echo_received, pulse_duration
    if pin.value() == 1:
        pulse_start = time.ticks_us()
    else:
        if not echo_late:
            echo_timeout.deinit()
            pulse_end = time.ticks_us()
            pulse_duration = pulse_end - pulse_start
            echo_received = True
        else:
            echo_late = False

def handle_timeout_echo(timer):
    global echo_late
    echo_late = True

pin_led_red: Pin = Pin(0, mode=Pin.OUT, value=0)
pin_led_green: Pin = Pin(1, mode=Pin.OUT, value=0)
pin_trigger = Pin(17, Pin.OUT)
pin_echo = Pin(16, Pin.IN, Pin.PULL_DOWN)
pin_echo.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=handle_echo)
distance_cm = '00'
pulse_start = None
echo_timeout: Timer = Timer()
echo_late = False
echo_received = False
pulse_duration = 0

def send_trigger():
    pin_trigger.on()
    time.sleep_us(10)
    pin_trigger.off()
    echo_timeout.init(period=50, mode=Timer.ONE_SHOT, callback=handle_timeout_echo)

def write_distance(echo_state, pulse_time, pin_red, pin_green):
    if echo_state and pulse_time:
        distance_cm = round(pulse_time * 17165 / 1000000, 0)
        print('Distance: {:.0f} cm'.format(distance_cm))
        if distance_cm < 30:
            pin_green.off()
            print("Alarm !!\n")
            pin_red.on()
            time.sleep_ms(500)
            pin_red.off()
        else:
            pin_green.on()

# async def toggle_led_red(led, condition):
#     if condition:
#         led.on()
#         time.sleep_ms(500)
#         led.off()

try:
    while True:
        send_trigger()
        write_distance(echo_received, pulse_duration, pin_led_red, pin_led_green)
        echo_received = False
        time.sleep(1)
except KeyboardInterrupt:
    pin_led_red.off
    pin_led_green.off()
    pin_echo.off()
    pin_trigger.off()
    print("EOP")
