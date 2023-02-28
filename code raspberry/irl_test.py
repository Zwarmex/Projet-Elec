from machine import Pin, Timer
import time

def handle_input(pin):
    global pin_led_green, pin_led_red, timeout_input, timestamp_start, timestamp_end
    print(time.ticks_us())
    if not pin.value():
        timestamp_start = time.ticks_us()
        # timeout_input.deinit()
        pin_led_red.on()
        pin_led_green.on()
    else:
        pin_led_red.off()
        pin_led_green.off()
        # init_timeout()
        timestamp_end = time.ticks_us()
    if timestamp_end and timestamp_start:
        print(f"diff : {time.ticks_diff(timestamp_end, timestamp_start)}")

# def init_timeout():
#     global timeout_input
#     if timeout_input:
#         timeout_input.deinit()
#     timeout_input: Timer = Timer()
#     timeout_input.init(mode=Timer.PERIODIC, period=1000, callback=handle_timeout)

def handle_timeout(timer):
    print(f"TIMEOUT : {timer} at {time.ticks_us()}")

pin_led_green: Pin = Pin(0, mode=Pin.OUT, value=0)
pin_led_red: Pin = Pin(1, mode=Pin.OUT, value=0)
pin_input: Pin = Pin(16, mode=Pin.IN, pull=Pin.PULL_UP)
pin_input.irq(handle_input, Pin.IRQ_RISING | Pin.IRQ_FALLING)
continue_running: bool = True
timeout_input = None
timestamp_start = None
timestamp_end = None
# init_timeout()

# while continue_running:
#     if pin_input.value():
#         pin_led_red.off()
#         pin_led_green.off()
#     else:
#         pin_led_red.on()
#         pin_led_green.on()
#     time.sleep(1)

