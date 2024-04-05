from machine import Pin
from servo import Servo
from BLDC import BLDCMotor
from Stepper import StepperMotor
import time

class MotionController:
    def __init__(self, servo1_pin, servo2_pin, pwm_pin, dir_pin1, dir_pin2, step1_pin, dir1_pin, step2_pin, dir2_pin):
        self.servo_motor1 = Servo(servo1_pin)
        self.servo_motor2 = Servo(servo2_pin)
        self.bldc_motor = BLDCMotor(pwm_pin, dir_pin1, dir_pin2)
        self.stepper_motor = StepperMotor(step1_pin, dir1_pin, step2_pin, dir2_pin)
        self.steps = 0
        self.servo_motor1.goto(0)
        self.servo_motor2.goto(1024)

    def run(self):
        value = 0
        value2 = 1024
        try:
            while value <= 904 and value2 >= 120:  
                self.servo_motor1.goto(value)
                self.servo_motor2.goto(value2)
                self.bldc_motor.set_speed(-100)
                time.sleep(0.015)  
                value += 4
                value2 -= 4  
                print("fhdhdhf")
                
            time.sleep(1.5)
            while value > 4 and value2 < 1020:
                self.servo_motor1.goto(value)
                self.servo_motor2.goto(value2)
                self.bldc_motor.set_speed(-100)
                time.sleep(0.015)
                value -= 4
                value2 += 4
                print("fhfhd")
                
            self.bldc_motor.set_speed(0)
            time.sleep(2)
            while self.steps < 4000:
                self.stepper_motor.stepper_up(2000)
                time.sleep(0.3)
                self.steps += 2000
                
        except KeyboardInterrupt:
            self.servo_motor1.free()
            self.servo_motor2.free()
            self.bldc_motor.stop()
