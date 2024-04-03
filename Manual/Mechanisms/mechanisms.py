from machine import Pin
from servo import Servo
from BLDC import BLDCMotor
from Stepper import StepperMotor
from Ultrasonic import UltrasonicSensor
import time

#roller servo
servo1_pin = 19
servo2_pin = 18

#gate servo
gate_servo_pin = 16

#push servo
push_servo_pin = 17

#roller dc motor
pwm_pin = 28
dir_pin1 = 27
dir_pin2 = 26

#elevator steppers
step1_pin = 13
dir1_pin = 12
step2_pin = 15
dir2_pin = 14

flag =2

#elevator ultrasonic
trigger_pin = 21  
echo_pin = 22

distance = 50

ultrasonic_sensor = UltrasonicSensor(trigger_pin, echo_pin)
servo_motor1 = Servo(servo1_pin)
servo_motor2 = Servo(servo2_pin)
gate_servo = Servo(gate_servo_pin)
push_servo = Servo(push_servo_pin)
bldc_motor = BLDCMotor(pwm_pin, dir_pin1, dir_pin2)
stepper_motor = StepperMotor(step1_pin, dir1_pin, step2_pin, dir2_pin)
steps = 0
servo_motor1.goto(0)
servo_motor2.goto(1024)
gate_servo.goto(0)
push_servo.goto(0)
mech_pico_signal_pin = Pin(11, Pin.IN)
stepper_up = 0 
while True:
    pin_value = mech_pico_signal_pin.value()
    if(pin_value == 1):
        print("Pin value:", pin_value)
    if(pin_value == 1 and flag !=1):
        print("Started Roller")
        bldc_motor.set_speed(-100)
        time.sleep(0.1)
        servo_motor1.goto(0)
        print("Servo 1 at : 0")
        servo_motor2.goto(1024)
        print("Servo 2 at: 1024")
        gate_servo.goto(500)
        flag = 1
        time.sleep(2)
#         while(distance>20):
#             distance = ultrasonic_sensor.measure_distance()
#             if(distance<20):
#                 distance = ultrasonic_sensor.measure_distance()
        stepper_motor.stepper_up(3900)
        stepper_up = 1
    elif(pin_value == 0 and flag !=0):
        servo_motor1.goto(860)
        servo_motor2.goto(164)
        bldc_motor.set_speed(0)
        flag = 0
        if(stepper_up == 1):
            stepper_motor.stepper_down(3500)
            stepper_up = 0
    time.sleep(0.01)

