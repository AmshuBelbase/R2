from machine import Pin
from servo import Servo
from BLDC import BLDCMotor
from Stepper import StepperMotor
from Ultrasonic import UltrasonicSensor
import time

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

flag = 2

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
mech_pico_signal_pin = Pin(11, Pin.IN)
stepper_up = 0 
while True:
    pin_value = mech_pico_signal_pin.value()
#     if (pin_value == 1):
#         print("Pin value:", pin_value)
    if (pin_value == 1 and flag != 1):
        print("Started Roller")
        bldc_motor.set_speed(-100)
        time.sleep(0.05)
        roller_servo_motor1.goto(0)
        print("Servo 1 at : 0")
        roller_servo_motor2.goto(1024)
        print("Servo 2 at: 1024")
        gate_servo.goto(350)
        
        flag = 1
        time.sleep(2)
#         while(distance>20):
#             distance = ultrasonic_sensor.measure_distance()
#             if(distance<20):
#                 distance = ultrasonic_sensor.measure_distance()
#         stepper_motor.stepper_up(8000)
        stepper_up = 1
        time.sleep(1)
        push_servo.goto(500)
    elif (pin_value == 0 and flag != 0 and stepper_up == 1):
        flag = 0
        push_servo.goto(1024)
#         stepper_motor.stepper_down(8000)
        gate_servo.goto(0)
        stepper_up = 0
        roller_servo_motor1.goto(860)
        roller_servo_motor2.goto(164)
        bldc_motor.set_speed(0)
    time.sleep(0.01)
