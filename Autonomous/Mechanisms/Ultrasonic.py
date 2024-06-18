from machine import Pin
import time

left_trig = Pin(20, Pin.OUT)   
left_echo = Pin(21, Pin.IN)

right_trig = Pin(18, Pin.OUT) 
right_echo = Pin(19, Pin.IN)

# roller_trig = Pin(22, Pin.OUT)
# roller_echo = Pin(26, Pin.IN)

elevator_trig = Pin(27, Pin.OUT)
elevator_echo = Pin(28, Pin.IN)

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

while True:
    print("loop")
    
    right_us = measure_distance(right_trig, right_echo) 
    print("Right: ", right_us)
    
    elevator_us = measure_distance(elevator_trig, elevator_echo)  
    print("Elevator: ", elevator_us)
    
    left_us = measure_distance(left_trig, left_echo) 
    print("Left: ", left_us)

    time.sleep_ms(1000)