from machine import Pin
from servo import Servo
from BLDC import BLDCMotor
from Stepper import StepperMotor
from Ultrasonic import UltrasonicSensor
import time
import utime
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

# Define the pin connected to the PWM signal
pwm_input_pin = machine.Pin(11, machine.Pin.IN)

stepper_up = 2
feed_in = 2
push_in = 2

feed_mech = 0
step_up = 0
step_down = 0
push_mech = 0

limit_list = [15, 30, 35, 45, 55, 63, 65, 75]

# Define a function to measure PWM duty cycle
def measure_pwm_duty_cycle(pin, duration=0.1):
    start_time = utime.ticks_us()
    while not pin.value():
        if utime.ticks_diff(utime.ticks_us(), start_time) > duration * 1000000:
            return None  # Timeout
    pulse_start = utime.ticks_us()
    while pin.value():
        if utime.ticks_diff(utime.ticks_us(), start_time) > duration * 1000000:
            return None  # Timeout
    pulse_end = utime.ticks_us()
    pulse_duration = utime.ticks_diff(pulse_end, pulse_start)
    period_duration = utime.ticks_diff(pulse_end, start_time)
    duty_cycle = (pulse_duration / period_duration) * 100
    return duty_cycle


while True:
    pwm_duty_cycle = measure_pwm_duty_cycle(pwm_input_pin)
    if pwm_duty_cycle is not None:    
        print("Received PWM Duty Cycle: {:.2f}%".format(pwm_duty_cycle))
        if (pwm_duty_cycle > limit_list[0] and pwm_duty_cycle < limit_list[1]):
            print("feed")
            feed_mech = 1
            step_up = 0
            step_down = 0
            push_mech = 0
        
        elif (pwm_duty_cycle > limit_list[2] and pwm_duty_cycle < limit_list[3]):
            print("step up")
            feed_mech = 0
            step_up = 1
            step_down = 0
            push_mech = 0
            
        elif (pwm_duty_cycle > limit_list[4] and pwm_duty_cycle < limit_list[5]):
            print("push")
            feed_mech = 0
            step_up = 0
            step_down = 0
            push_mech = 1
        elif (pwm_duty_cycle > limit_list[6] and pwm_duty_cycle < limit_list[7]):
            print("step down")
            feed_mech = 0
            step_up = 0
            step_down = 1
            push_mech = 0    
        else:
            print("no mech")
            feed_mech = 0
            step_up = 0
            step_down = 0
            push_mech = 0
        
        if(feed_mech == 0):
            print("Stopped Roller")
            bldc_motor.set_speed(0)  
#             print("Servo 1 at : 860") 
#             print("Servo 2 at: 164")
            roller_servo_motor1.goto(860)
            roller_servo_motor2.goto(164)
            gate_servo.goto(0)
            feed_in = 0
            
        if(push_mech == 0):
            push_servo.goto(1024)
    
        if(feed_mech == 1 and step_up == 0 and step_down == 0 and push_mech == 0):
            print("Started Roller")
            bldc_motor.set_speed(-100)
            time.sleep(0.05)
            roller_servo_motor1.goto(0)
#             print("Servo 1 at : 0")
            roller_servo_motor2.goto(1024)
#             print("Servo 2 at: 1024")
            gate_servo.goto(350) 
            
        elif(feed_mech == 0 and step_up == 1 and step_down == 0 and push_mech == 0):
#             stepper_motor.stepper_up(500)
            print("steps")
        
        elif(feed_mech == 0 and step_up == 0 and step_down == 1 and push_mech == 0):
#             stepper_motor.stepper_down(500)
            print("steps")
            
        elif(feed_mech == 0 and step_up == 0 and step_down == 0 and push_mech == 1):
            push_servo.goto(500)
    
    else:
        pwm_duty_cycle = 0.0
#         print("Received PWM Duty Cycle: {:.2f}%".format(pwm_duty_cycle))
    time.sleep(0.01)

