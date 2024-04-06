import machine
import utime

# Define the GPIO pins available on the Pico
pins = [machine.Pin(pin_num, machine.Pin.OUT) for pin_num in range(28)]

while(True):
    print("high")
    # Set all pins to high
    for pin in pins:
        pin.high()
    
    # Wait for a few seconds to observe the state
    utime.sleep(1)
    print("low")
    # Optional: Reset all pins to low
    for pin in pins:
        pin.low()
    utime.sleep(1)
