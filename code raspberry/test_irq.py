from machine import Pin, Timer
import utime

def format_distance(distance: float):
    return "%02d" % distance

def handle_echo(pin):
    global timeout_echo
    timeout_echo.deinit()
    global echo_received
    echo_received = True
    

def handle_timeout_echo(time):
    global echo_timeout
    echo_timeout = True

def send_trigger():
    global trigger_sent
    global timestamp_trig
    global timeout_echo
    timestamp_trig = utime.ticks_us()
    trigger_sent = True
    timeout_echo = Timer()
    pin_hc_echo.value(1)
    timeout_echo.init(period=50, mode=Timer.ONE_SHOT, callback=handle_timeout_echo)

pin_hc_echo: Pin = Pin(27, mode=Pin.IN)
pin_hc_echo.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=handle_echo)
continue_running: bool = True
echo_received: bool = False
trigger_sent: bool = False
echo_timeout = True
timeout_echo: Timer = Timer()
distance_cm: str = '00'

while continue_running:
    if echo_received:
        print("echo received")
        timestamp_echo = utime.ticks_us()
        print(f"\033cdiff : {timestamp_echo - timestamp_trig}")
        print(f"trig : {timestamp_trig}")
        print(f"echo : {timestamp_echo}")
        echo_received = False
        continue_running = False
    elif echo_timeout:
        print("timeout echo :(")
    if not trigger_sent:
        utime.sleep(2)
        send_trigger()
        trigger_sent = False



