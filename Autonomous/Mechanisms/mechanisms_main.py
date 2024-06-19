from machine import Pin, UART, PWM
from servo import Servo 
from Stepper import StepperMotor 
import time
import utime

# ----------------- PINOUTS -----------------

uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))  

# roller servo
roller_servo_r_pin = 11
roller_servo_l_pin = 10
roller_servo1 = Servo(roller_servo_r_pin)
roller_servo2 = Servo(roller_servo_l_pin)

# gate servo
gate_servo_r_pin = 7
gate_servo_l_pin = 6
gate_servo1 = Servo(gate_servo_r_pin)
gate_servo2 = Servo(gate_servo_l_pin)

# push servo
push_servo_r_pin = 3
push_servo_l_pin = 2
push_servo1 = Servo(push_servo_r_pin)
push_servo2 = Servo(push_servo_l_pin)
 

# roller dc motor
roller_pin1 = Pin(15, Pin.OUT)
roller_pin2 = Pin(14, Pin.OUT)

# elevator steppers
elevator_step1_pin = 16
elevator_dir1_pin = 17
stepper_motor = StepperMotor(elevator_step1_pin, elevator_dir1_pin)

#ultrasonics
left_trig = Pin(20, Pin.OUT)   
left_echo = Pin(21, Pin.IN)

right_trig = Pin(18, Pin.OUT) 
right_echo = Pin(19, Pin.IN)

# roller_trig = Pin(27, Pin.OUT)
# roller_echo = Pin(28, Pin.IN)

# elevator_trig = Pin(27, Pin.OUT)
# elevator_echo = Pin(28, Pin.IN)



# ----------------- INITIAL POSITIONS -----------------

gate_servo1.goto(100) 
gate_servo2.goto(900)

push_servo1.goto(0) 
push_servo2.goto(1000)

roller_pin1.value(1)
roller_pin2.value(0)

x_deg = 700    # 150
y_deg = 1024 - x_deg
roller_servo1.goto(x_deg) 
roller_servo2.goto(y_deg)

time.sleep(1)

roller_pin1.value(0)
roller_pin2.value(0)

# ----------------- GLOBAL AVRIABLES -----------------

drive_stat = 0


# ----------------- USER DEFINED FUNCTIONS -----------------

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


# ----------------- MAIN CODE -----------------

while True:
    if uart.any():
        print("received")
        message_bytes = uart.read()
        message = message_bytes.decode('utf-8')
        li = list(message.split(","))
        if(len(li) == 1): 
            drive_stat = int(li[0])
        else:
            continue
        print(drive_stat)
    if(drive_stat == 1):
        roller_pin1.value(1)
        roller_pin2.value(0)
        x_deg = roller_servo1.get_position() 
        roller = 100
        while x_deg != roller:
            if(x_deg > roller):
                x_deg = x_deg -1
            else:
                x_deg = x_deg +1 
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)
            time.sleep_us(1000)
            
        right_us = measure_distance(right_trig, right_echo) 
        print("Right: ", right_us) 
        
        left_us = measure_distance(left_trig, left_echo) 
        print("Left: ", left_us)
