from machine import Pin, UART, PWM
from servo import Servo
from BLDC import BLDCMotor
from Stepper import StepperMotor
from Ultrasonic import UltrasonicSensor
import time
import utime


uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))  

# roller servo
roller_servo1_pin = 19
roller_servo2_pin = 18

# gate servo
gate_servo_pin = 17

# push servo
push_servo_pin = 16

# roller dc motor
pwm_pin = 27
dc_dir_pin1 = 26
dc_dir_pin2 = 28

# elevator steppers
elevator_step1_pin = 13
elevator_dir1_pin = 12
elevator_step2_pin = 15
elevator_dir2_pin = 14
 

# elevator ultrasonic
trigger_pin = 21
echo_pin = 22

distance = 50

ultrasonic_sensor = UltrasonicSensor(trigger_pin, echo_pin)
roller_servo_motor1 = Servo(roller_servo1_pin)
roller_servo_motor2 = Servo(roller_servo2_pin)
gate_servo = Servo(gate_servo_pin)
push_servo = Servo(push_servo_pin)
bldc_motor = BLDCMotor(pwm_pin, dc_dir_pin1, dc_dir_pin2)
stepper_motor = StepperMotor(
    elevator_step1_pin, elevator_dir1_pin, elevator_step2_pin, elevator_dir2_pin)
steps = 0
x_deg = 900
y_deg = 1024 - x_deg
roller_servo_motor1.goto(x_deg)
roller_servo_motor2.goto(y_deg)
gate_servo.goto(0)
push_servo.goto(1024)
bldc_motor.set_speed(0)

stepper_up = 0
 

while True:
    if uart.any():
        message_bytes = uart.read()
        message = message_bytes.decode('utf-8')
        li = list(message.split(","))
        if(len(li) <= 3): 
            step_up_down, feed_mech, push_mech = int(li[0]), int(li[1]), int(li[2])
        else:
            continue
        print(step_up_down, feed_mech, push_mech)
        if(feed_mech < -50):
            print("feed_mech on")
            print("Started Roller")
            bldc_motor.set_speed(-100)
            time.sleep(0.05)
            roller_servo_motor1.goto(0) 
            roller_servo_motor2.goto(1024) 
            gate_servo.goto(350) 
        else:  
            bldc_motor.set_speed(0)   
            roller_servo_motor1.goto(860)
            roller_servo_motor2.goto(164)
            gate_servo.goto(0)
            
        if(step_up_down < -80 and stepper_up == 0):
            print("step_up")
            stepper_motor.stepper_up(4000)
            stepper_up = 1
        elif(step_up_down > 80 and stepper_up == 1):
            print("step_down")
            stepper_motor.stepper_down(4000)
            stepper_up = 0
            
        if(push_mech > 50):
            print("push_mech on")
            push_servo.goto(500)
        else: 
            push_servo.goto(1024)
    else:
        print("Waiting")
    time.sleep(0.01)
 