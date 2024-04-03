from machine import Pin, PWM, UART
from ibus import IBus
import utime
# from servo import Servo  # Importing the Servo class from the servo module
# from BLDC import BLDCMotor
# from Stepper import StepperMotor


# from movementmechanism import MotionController

servo1_pin = 16
servo2_pin = 17

step1_pin = 13
dir1_pin = 12 #stepper direction
step2_pin = 15
dir2_pin = 14 #stepper direction

pwm_pin = 28
dir_pin1 = 27
dir_pin2 = 26



# Create an instance of the MotionController class
# motion_controller = MotionController(servo1_pin, servo2_pin, pwm_pin, dir_pin1, dir_pin2, step1_pin, dir1_pin, step2_pin, dir2_pin)


ibus_in = IBus(1)

    

while True:
    res = ibus_in.read()
    # if signal then display immediately
    if res[0] == 1:
        print("Status {} CH 1 {} Ch 2 {} Ch 3 {} Ch 4 {} Ch 5 {} Ch 6 {} - {}".format(
            res[0],
            IBus.normalize(res[1]),
            IBus.normalize(res[2]),
            IBus.normalize(res[3]),
            IBus.normalize(res[4]),
            IBus.normalize(res[5]),
            IBus.normalize(res[6]),
            utime.ticks_ms()
        ))
#                
#     val = IBus.normalize(res[5])
#     if val>10:
#         motion_controller.run()
#     utime.sleep_ms(10)