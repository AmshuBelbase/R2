from machine import Pin, PWM
from servo import Servo  # Importing the Servo class from the servo module
from BLDC import BLDCMotor
from Stepper import StepperMotor
import time


# Define the GPIO pin connected to the servo motors
step1=Pin(13,Pin.OUT)
dir1=Pin(12,Pin.OUT)

step2=Pin(15,Pin.OUT)
dir2=Pin(14,Pin.OUT)
stepper_motor = StepperMotor(step1, dir1, step2, dir2)
servo1_pin = 19  # Example pin number, change it to match your setup
servo2_pin = 18
PWM_PIN = 28  # PWM pin for speed control
DIR_PIN1 = 27  # Direction pin 1
DIR_PIN2 = 26  # Direction pin 2
steps=0
servo3_pin = 16
# Create an instance of the Servo class with the servo pins
servo_motor1 = Servo(servo1_pin)
servo_motor2 = Servo(servo2_pin)
servo_motor3 = Servo(servo3_pin)

servo_motor1.goto(0)
servo_motor2.goto(1024)
servo_motor3.goto(300)
bldc_motor = BLDCMotor(PWM_PIN, DIR_PIN1, DIR_PIN2)
value=0
value2=1024
try:
    
    
    while value <= 904 and value2 >= 120:  # Update the condition to ensure both servos move forward
        # Move the servo motors by 5.68 every 10 milliseconds
        servo_motor1.goto(value)
        servo_motor2.goto(value2)
        #bldc_motor.set_speed(-100)
        time.sleep(0.015)  # Adjust the delay as needed
        value += 4
        value2 -= 4  # Increment value2 to move servo_motor2 forward
        print("fhdhdhf")
        
    time.sleep(1.5)
    while value>4 and value2<1020:
        servo_motor1.goto(value)
        servo_motor2.goto(value2)
        #bldc_motor.set_speed(-100)
        time.sleep(0.015)
        value -= 4
        value2 += 4
        print("fhfhd")
        
    bldc_motor.set_speed(0)
    time.sleep(1)
    servo_motor3.goto(0)
    stepper_motor.stepper_up(4100)
        
    
except KeyboardInterrupt:
    # Stop the servo motors and deinitialize PWM on Ctrl+C
    servo_motor1.free()
    servo_motor2.free()
    bldc_motor.stop()

