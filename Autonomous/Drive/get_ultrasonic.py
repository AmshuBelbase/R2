from machine import Pin
import time
 
trigger = Pin(17, Pin.OUT)
echo = Pin(16, Pin.IN)

def measure_distance(trigger, echo):
    # Send a 10us pulse to trigger the sensor
    trigger.off()
    time.sleep_us(2)
    trigger.on()
    time.sleep_us(10)
    trigger.off()

    # Wait for the echo to start
    while echo.value() == 0:
        pass
    start_time = time.ticks_us()

    # Wait for the echo to end
    while echo.value() == 1:
        pass
    end_time = time.ticks_us()

    # Calculate the duration of the echo pulse
    duration = time.ticks_diff(end_time, start_time)

    # Convert the duration to distance (in cm)
    # Speed of sound = 343 m/s = 34300 cm/s
    # Distance = (duration * speed of sound) / 2
    distance = duration * 34300 / (2 * 1000000)  # Convert microseconds to seconds

    return distance

while True:
    us_val = measure_distance(trigger, echo)
    print("Distance:", us_val)
    time.sleep_us(100)
