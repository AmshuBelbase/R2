from machine import Pin
from servo import Servo
from BLDC import BLDCMotor
from Stepper import StepperMotor
import time
from ibus import IBus

servo1_pin = 16
servo2_pin = 17
pwm_pin = 28
dir_pin1 = 27
dir_pin2 = 26
step1_pin = 13
dir1_pin = 12
step2_pin = 15
dir2_pin = 14
flag =2

ibus_in = IBus(1)

while True:
    res = ibus_in.read()
        if res[0] == 1:
        val = IBus.normalize(res[5])
        print(val)
            if val == 0 and flag !=1:

                bldc_motor.set_speed(-100)
                time.sleep(0.5)
                servo_motor1.goto(0)
                servo_motor2.goto(1024)
                flag =1

            elif val == -100 and flag !=0:
                servo_motor1.goto(860)
                servo_motor2.goto(164)
                flag =0
