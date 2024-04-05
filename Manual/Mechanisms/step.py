from machine import Pin 
from Stepper import StepperMotor 
import time
 
# elevator steppers
elevator_step1_pin = 13
elevator_dir1_pin = 12
elevator_step2_pin = 15
elevator_dir2_pin = 14

stepper_motor = StepperMotor(
    elevator_step1_pin, elevator_dir1_pin, elevator_step2_pin, elevator_dir2_pin)
steps = 0  
stepper_up = 0
# while True: 
print("Started Stepper")
stepper_motor.stepper_up(3900)
time.sleep(0.01)

