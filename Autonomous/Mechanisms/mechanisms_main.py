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

roller_trig = Pin(22, Pin.OUT)
roller_echo = Pin(26, Pin.IN)

elevator_trig = Pin(27, Pin.OUT)
elevator_echo = Pin(28, Pin.IN)

# left_trig = Pin(20, Pin.OUT)   
# left_echo = Pin(21, Pin.IN)
# 
# right_trig = Pin(18, Pin.OUT) 
# right_echo = Pin(19, Pin.IN)


# ----------------- INITIAL POSITIONS -----------------

drive_stat = 30
message = "{}".format(drive_stat)
print("Sent: ",message)
message_bytes = message.encode('utf-8')
uart.write(message_bytes)

gate_servo1.goto(700) 
gate_servo2.goto(300)

push_servo1.goto(700) 
push_servo2.goto(300)

roller_pin1.value(0)
roller_pin2.value(0)
 
x_deg = roller_servo1.get_position() 
roller = 700
while x_deg != roller:
    if(x_deg > roller):
        x_deg = x_deg -1
    else:
        x_deg = x_deg +1 
    y_deg = 1024 - x_deg
    roller_servo1.goto(x_deg) 
    roller_servo2.goto(y_deg)
    time.sleep_us(1000)

stepper_motor.stepper_up(2150)
time.sleep(0.1)
stepper_motor.stepper_down(2150)
push_servo1.goto(0) 
push_servo2.goto(1000) 

roller_pin1.value(1)
roller_pin2.value(0)

time.sleep_ms(300)

roller_pin1.value(0)
roller_pin2.value(0)        

# ----------------- GLOBAL AVRIABLES -----------------

drive_stat = 3

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

led_pin = Pin(25, Pin.OUT)
led_pin.value(1)


# time.sleep(1) 

while True:
    if uart.any(): 
        message_bytes = uart.read()
        message = message_bytes.decode('utf-8')
        li = list(message.split(","))
        if(len(li) == 1): 
            drive_stat = int(li[0])
        else:
            continue
        print("Received: ",drive_stat)
    if(drive_stat == 1):
        roller_pin1.value(0)
        roller_pin2.value(0)
        gate_servo1.goto(100) 
        gate_servo2.goto(900)
        x_deg = roller_servo1.get_position() 
        roller = 500
        while x_deg != roller:
            if(x_deg > roller):
                x_deg = x_deg -1
            else:
                x_deg = x_deg +1 
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)
            time.sleep_us(1000)
    if(drive_stat == 2): 
        roller_pin1.value(1)
        roller_pin2.value(0)
        x_deg = roller_servo1.get_position() 
        roller = 0
        while x_deg != roller:
            if(x_deg > roller):
                x_deg = x_deg -1
            else:
                x_deg = x_deg +1 
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)
            time.sleep_us(1000)
    if drive_stat == 8:
        stepper_motor.stepper_up(900)
        push_servo1.goto(0) 
        push_servo2.goto(1000)
        time.sleep(1)
        stepper_motor.stepper_down(2150)
        push_servo1.goto(700) 
        push_servo2.goto(300)
        drive_stat = 9
        message = "{}".format(drive_stat)
        print("Sent: ",message)
        message_bytes = message.encode('utf-8')
        uart.write(message_bytes)
    if(drive_stat == 3 or drive_stat == 4):
        
        if drive_stat == 3: # if red or blue ball then feed
            gate_servo1.goto(100) 
            gate_servo2.goto(900)
        elif drive_stat == 4: # if purple ball then discard
            gate_servo1.goto(700) 
            gate_servo2.goto(300)
            
        roller_pin1.value(1)
        roller_pin2.value(0)
        
        print("At 150")
        x_deg = 150    # 150
        y_deg = 1024 - x_deg
        roller_servo1.goto(x_deg) 
        roller_servo2.goto(y_deg)

        time.sleep(1)  

        print("At 350")
        x_deg = 350    # 150
        y_deg = 1024 - x_deg
        roller_servo1.goto(x_deg) 
        roller_servo2.goto(y_deg)

        c = 0
        start_time = utime.ticks_ms()
        while utime.ticks_diff(utime.ticks_ms(), start_time) < 2500:  # 3000 ms = 3 seconds
            roller_us = measure_distance(roller_trig, roller_echo)
            print("roller_us: ", roller_us)
            
            if roller_us < 10:
                start_time = utime.ticks_ms()
                c += 1
            else:
                c = 0
            
            time.sleep_ms(10)

            # Check if c has been incremented 60 times (meaning elevator < 4 for 60 consecutive iterations)
            if c > 40:
                break

        # If loop terminated due to timeout
        if utime.ticks_diff(utime.ticks_ms(), start_time) >= 2500:
            print("Loop terminated due to timeout.")
            roller_pin1.value(0)
            roller_pin2.value(1)
            print("At 0")
            x_deg = 0    # 150
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)

#             time.sleep(0.5)
            
            drive_stat = 4  
        else:
            print("At 500")
            x_deg = 500    # 150
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)

            time.sleep(0.5)


            print("At 1000")
            x_deg = 1000    # 150
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)
        
        if drive_stat == 4: # if purple ball then again start searching
            drive_stat = 5
            message = "{}".format(drive_stat)
            print("Sent: ",message)
            message_bytes = message.encode('utf-8')
            uart.write(message_bytes)
            time.sleep(1)
        else:                
            c = 0
            start_time = utime.ticks_ms()
            while utime.ticks_diff(utime.ticks_ms(), start_time) < 4500:  # 3000 ms = 3 seconds
                elevator = measure_distance(elevator_trig, elevator_echo)
                print("elevator: ", elevator)
                
                if elevator < 10:
                    start_time = utime.ticks_ms()
                    c += 1
                else:
                    c = 0
                
                time.sleep_ms(5)

                # Check if c has been incremented 60 times (meaning elevator < 4 for 60 consecutive iterations)
                if c > 40:
                    break

            # If loop terminated due to timeout
            if utime.ticks_diff(utime.ticks_ms(), start_time) >= 4500:
                print("Loop terminated due to timeout.")
                drive_stat = 5
                message = "{}".format(drive_stat)
                print("Sent: ",message)
                message_bytes = message.encode('utf-8')
                uart.write(message_bytes)
            else:
                gate_servo1.goto(700) 
                gate_servo2.goto(300)
                push_servo1.goto(700) 
                push_servo2.goto(300)
                
                stepper_motor.stepper_up(1250)
                
                drive_stat = 6
                message = "{}".format(drive_stat)
                print("Sent: ",message)
                message_bytes = message.encode('utf-8')
                uart.write(message_bytes)
                
                print("At 500")
                x_deg = 500    # 150
                y_deg = 1024 - x_deg
                roller_servo1.goto(x_deg) 
                roller_servo2.goto(y_deg)
        roller_pin1.value(0)
        roller_pin2.value(0)
#                 time.sleep(1)
#                 stepper_motor.stepper_up(900)
#                 push_servo1.goto(0) 
#                 push_servo2.goto(1000)
#                 time.sleep(1)
#                 stepper_motor.stepper_down(2150)
#                 push_servo1.goto(700) 
#                 push_servo2.goto(300)
        
         





