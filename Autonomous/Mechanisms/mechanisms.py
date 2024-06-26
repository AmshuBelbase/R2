from machine import Pin, UART, PWM
from servo import Servo 
from Stepper import StepperMotor 
import time
import utime

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

# front ball ultrasonics 
# front_ball_left_trig = Pin(5, Pin.OUT)
# front_ball_left_echo = Pin(4, Pin.IN)
# 
# front_ball_right_trig = Pin(2, Pin.OUT)
# front_ball_right_echo = Pin(3, Pin.IN)

drive_stat = 0 
steps = 0

gate_servo1.goto(700) 
gate_servo2.goto(300)

push_servo1.goto(1000) 
push_servo2.goto(0)


x_deg = 20    # 150
y_deg = 1024 - x_deg
roller_servo1.goto(x_deg) 
roller_servo2.goto(y_deg) 

roller_pin1.value(1)
roller_pin2.value(0)

x_deg = roller_servo1.get_position()  

roller = 1000
roller = 50
while x_deg != roller:
    if(x_deg > roller):
        x_deg = x_deg -1
    else:
        x_deg = x_deg +1 
    y_deg = 1024 - x_deg
    roller_servo1.goto(x_deg) 
    roller_servo2.goto(y_deg)
    time.sleep_us(1000)
 

#throw ball sequence
roller_pin1.value(1)
roller_pin2.value(0)
gate_servo1.goto(110) 
gate_servo2.goto(890)
roller = 1000
while x_deg != roller:
    if(x_deg > roller):
        x_deg = x_deg -1
    else:
        x_deg = x_deg +1 
    y_deg = 1024 - x_deg
    roller_servo1.goto(x_deg) 
    roller_servo2.goto(y_deg)
    time.sleep_us(1000)
time.sleep(1)
# gate_servo1.goto(500) 
# gate_servo2.goto(500)
roller_pin1.value(0)
roller_pin2.value(0)
stepper_motor.stepper_up(2050)
push_servo1.goto(0) 
push_servo2.goto(1000)
time.sleep(2)
stepper_motor.stepper_down(2050)
push_servo1.goto(1000) 
push_servo2.goto(0)
    
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


while False:
    if uart.any():
        print("received")
        message_bytes = uart.read()
        message = message_bytes.decode('utf-8')
        li = list(message.split(","))
        if(len(li) == 1): 
            drive_stat = int(li[0])
        else:
            continue
    if(drive_stat == 8):
        print("Search Code Received")
        x_deg = roller_servo1.get_position() 
        while x_deg != 150:
            if(x_deg > 150):
                x_deg = x_deg -1
            else:
                x_deg = x_deg +1 
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)
        print("Started Roller")
        roller_pin1.value(1)
        roller_pin2.value(0)
        time.sleep(3)
        print("Reverse Roller")
        roller_pin1.value(0)
        roller_pin2.value(1)
        time.sleep(3)
    if(drive_stat == 1):
        print("loop")
        x_deg = roller_servo1.get_position() 
        while x_deg != 150:
            if(x_deg > 150):
                x_deg = x_deg -1
            else:
                x_deg = x_deg +1 
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)
            
        front_ball_right_us = measure_distance(front_ball_right_trig, front_ball_right_echo)
        print("Front Ball at right: ", front_ball_right_us)
        
        front_ball_left_us = measure_distance(front_ball_left_trig, front_ball_left_echo)
        print("Front Ball at left: ", front_ball_left_us)
        if((front_ball_left_us < 13 or front_ball_right_us < 13) and (front_ball_left_us > 2 and front_ball_right_us > 2)): # front_ball_left_us < 15 and front_ball_right_us < 15
            drive_stat = 0
            message = "{}".format(drive_stat)
            print(message)
            message_bytes = message.encode('utf-8')
            uart.write(message_bytes)
            
            print("Started Roller")
            roller_pin1.value(1)
            roller_pin2.value(0)
            time.sleep(0.75)
            
            x_deg = roller_servo1.get_position() 
            while x_deg != 950:
                if(x_deg > 950):
                    x_deg = x_deg -1
                else:
                    x_deg = x_deg +1 
                y_deg = 1024 - x_deg
                roller_servo1.goto(x_deg) 
                roller_servo2.goto(y_deg)
                time.sleep_us(1000)
            time.sleep(3)
            
            drive_stat = 1
            message = "{}".format(drive_stat)
            print(message)
            message_bytes = message.encode('utf-8')
            uart.write(message_bytes)
        else:
            roller_pin1.value(0)
            roller_pin2.value(0)
            
            x_deg = roller_servo1.get_position() 
            while x_deg != 150:
                if(x_deg > 150):
                    x_deg = x_deg -1
                else:
                    x_deg = x_deg +1 
                y_deg = 1024 - x_deg
                roller_servo1.goto(x_deg) 
                roller_servo2.goto(y_deg)
                time.sleep_us(1000)
                
#             drive_stat = 1
#             message = "{}".format(drive_stat)
#             print(message)
#             message_bytes = message.encode('utf-8')
#             uart.write(message_bytes)

            time.sleep(2)
        time.sleep_ms(90)
    time.sleep_ms(5)


















# 
# # gate servo
# gate_servo_pin = 16
# 
# # push servo
# push_servo_pin = 17
# 
# # roller dc motor
# roller_pin1 = Pin(27, Pin.OUT)
# roller_pin2 = Pin(28, Pin.OUT)
# 
# # elevator steppers
# elevator_step1_pin = 11
# elevator_dir1_pin = 10
# 
#  
# 
# # elevator ultrasonic
# trigger_pin = 21
# echo_pin = 22
# 
# distance = 50
# 
# ultrasonic_sensor = UltrasonicSensor(trigger_pin, echo_pin)
# roller_servo1 = Servo(roller_servo1_pin)
# roller_servo2 = Servo(roller_servo2_pin)
# gate_servo = Servo(gate_servo_pin)
# push_servo = Servo(push_servo_pin)
# stepper_motor = StepperMotor(elevator_step1_pin, elevator_dir1_pin)
# steps = 0
# x_deg = 900
# y_deg = 1024 - x_deg
# roller_servo1.goto(x_deg)
# roller_servo2.goto(y_deg)
# gate_servo.goto(0)
# push_servo.goto(500) 
# 
# stepper_up = 0
#  
# 
# while True:
#     if uart.any():
#         message_bytes = uart.read()
#         message = message_bytes.decode('utf-8')
#         li = list(message.split(","))
#         if(len(li) <= 3): 
#             step_up_down, feed_mech, push_mech = int(li[0]), int(li[1]), int(li[2])
#         else:
#             continue
#         print(step_up_down, feed_mech, push_mech)
#         if(feed_mech < -50 and stepper_up == 0):
#             print("feed_mech on")
#             print("Started Roller")
#             roller_pin1.value(1)
#             roller_pin2.value(0)
#             time.sleep(0.05)
# #             gate_servo.goto(350) 
#             roller_servo1.goto(0) 
#             roller_servo2.goto(1024)             
#         elif(stepper_up == 1):  
#             roller_servo1.goto(312)
#             roller_servo2.goto(712)
#         else:
#             roller_pin1.value(0)
#             roller_pin2.value(0)
#             roller_servo1.goto(860)
#             roller_servo2.goto(164)
#             
#             
#         if(step_up_down < -80 and stepper_up == 0):
#             print("step_up")
#             roller_servo1.goto(312)
#             roller_servo2.goto(712)
#             gate_servo.goto(0)
#             push_servo.goto(500) 
#             stepper_motor.stepper_up(2050)
#             stepper_up = 1
#         elif(step_up_down > 80 and stepper_up == 1):
#             print("step_down")
#             gate_servo.goto(0)
#             push_servo.goto(500) 
#             stepper_motor.stepper_down(2050) 
#             stepper_up = 0
#     
#         if(push_mech > 50):
#             print("push_mech on")
#             push_servo.goto(1024)
#             gate_servo.goto(350) 
#         else: 
#             push_servo.goto(500)
#             gate_servo.goto(0)
#     else:
#         print("Waiting")
#     time.sleep(0.01)
 










