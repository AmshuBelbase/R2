from machine import Pin, PWM, UART 
import time
mech_pico_signal_pin = Pin(15, Pin.IN)

while True:
    time.sleep(2)
    mech_pico_signal_pin.value(1)
#     print("HIGH")
#     time.sleep(2)
#     mech_pico_signal_pin.value(0)
#     print("LOW")