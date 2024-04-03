from machine import Pin, PWM, UART
from ibus import IBus
import time
mech_pico_signal_pin = Pin(26, Pin.OUT)

while True:
    time.sleep(2)
    mech_pico_signal_pin.value(1)
    print("HIGH")
    time.sleep(2)
    mech_pico_signal_pin.value(0)
    print("LOW")