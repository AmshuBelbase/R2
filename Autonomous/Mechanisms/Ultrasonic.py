from machine import Pin
import time, utime

elevator_trig = Pin(20, Pin.OUT)
elevator_echo = Pin(15, Pin.IN)


led_pin = Pin(25, Pin.OUT)
led_pin.value(1)

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

    # Distance = (duration * speed of sound) / 2
    distance = duration * 34300 / (2 * 1000000)  # Convert microseconds to seconds

    return distance

 
c = 0
start_time = utime.ticks_ms()

while utime.ticks_diff(utime.ticks_ms(), start_time) < 5000:  # 3000 ms = 3 seconds
    elevator = measure_distance(elevator_trig, elevator_echo)
    print("elevator: ", elevator)
    print(start_time)
    if elevator < 4:
        start_time = utime.ticks_ms()
        c += 1
    else:
        c = 0
    
    time.sleep_ms(10)

    # Check if c has been incremented 60 times (meaning elevator < 4 for 60 consecutive iterations)
    if c > 60:
        break
    

# If loop terminated due to time, print a message
if utime.ticks_diff(utime.ticks_ms(), start_time) >= 5000:
    print("Loop terminated due to timeout.")
else:
    print("Found Ball")