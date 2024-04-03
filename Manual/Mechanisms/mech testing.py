from machine import Pin
from servo import Servo
from BLDC import BLDCMotor
from Stepper import StepperMotor
import time
from ibus import IBus
from Ultrasonic import UltrasonicSensor


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
trigger_pin = 21  
echo_pin = 22 
distance = 50

ultrasonic_sensor = UltrasonicSensor(trigger_pin, echo_pin)
servo_motor1 = Servo(servo1_pin)
servo_motor2 = Servo(servo2_pin)
bldc_motor = BLDCMotor(pwm_pin, dir_pin1, dir_pin2)
stepper_motor = StepperMotor(step1_pin, dir1_pin, step2_pin, dir2_pin)
steps = 0
servo_motor1.goto(0)
servo_motor2.goto(1024)

mech_pico_signal_pin = Pin(11, Pin.IN)

while True:
    pin_value = mech_pico_signal_pin.value() 
    print("Pin value:", pin_value)
    if(pin_value == 1 and flag !=1):
        print("Started Roller")
        bldc_motor.set_speed(-100)
        time.sleep(0.05)
        servo_motor1.goto(0)
        print("Servo 1 at : 0")
        servo_motor2.goto(1024)
        print("Servo 2 at: 1024")
        flag = 1
        while(distance>20):
            distance = ultrasonic_sensor.measure_distance()
            if(distance<20):
                distance = ultrasonic_sensor.measure_distance()
        stepper_motor.stepper_up(3500)
    elif(pin_value == 0 and flag !=0):
        servo_motor1.goto(860)
        servo_motor2.goto(164)
        bldc_motor.set_speed(0)
        flag = 0
        stepper_motor.stepper_down(3500)
    time.sleep(0.01)
