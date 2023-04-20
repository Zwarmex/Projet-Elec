from machine import Pin
import time


def write_distance(distance: str, displays_array: list) -> None:
    state_display_left: str = get_pins(int(distance[0]))
    state_display_right: str = get_pins(int(distance[1]))
    for index in range(len(displays_array[0])):
        displays_array[0][index].value(int(state_display_left[index]))
    for index in range(len(displays_array[1])):
        displays_array[1][index].value(int(state_display_right[index]))
    print(f'{distance}')
    
def get_pins(number: int) -> str:
    pins_state: list = ["1111110", "0110000", "1101101", "1111001", "0110011",
                        "1011011", "1011111", "1110000", "1111111", "1111011"]
    return pins_state[number]
def calculate_distance(number: int) -> str:
    return "%02d" % (number)

#################INIT################
led=Pin("LED", Pin.OUT, value=0)    #
led(1)                              #
time.sleep(0.5)                     #
led(0)                              #
#####################################

displays: list= [[],[]] # left, right
for i in range(7):
    displays[0].append(Pin(9+i, Pin.OUT, value=0))
for i in range(7):
    displays[1].append(Pin(16+i, Pin.OUT, value=0))
try:
    for i in range (35):
        write_distance(calculate_distance(i), displays)
        time.sleep(0.5)
except KeyboardInterrupt:
    for display in displays:
        for pin in display:
            pin.off()