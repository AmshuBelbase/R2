from machine import Pin, UART, PWM
from servo import Servo 
from Stepper import StepperMotor
from Ultrasonic import UltrasonicSensor
import time
import utime


uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))  

# roller servo
roller_servo1_pin = 19
roller_servo2_pin = 18

# gate servo
gate_servo_pin = 16

# push servo
push_servo_pin = 17

# roller dc motor
roller_pin1 = Pin(27, Pin.OUT)
roller_pin2 = Pin(28, Pin.OUT)

# elevator steppers
elevator_step1_pin = 11
elevator_dir1_pin = 10

 

# elevator ultrasonic
trigger_pin = 21
echo_pin = 22

distance = 50

ultrasonic_sensor = UltrasonicSensor(trigger_pin, echo_pin)
roller_servo1 = Servo(roller_servo1_pin)
roller_servo2 = Servo(roller_servo2_pin)
gate_servo = Servo(gate_servo_pin)
push_servo = Servo(push_servo_pin)
stepper_motor = StepperMotor(elevator_step1_pin, elevator_dir1_pin)
steps = 0
x_deg = 900
y_deg = 1024 - x_deg
# roller_servo1.goto(x_deg)
# roller_servo2.goto(y_deg)
x_deg = roller_servo1.get_position()

while x_deg != 1024:
    if(x_deg > 1024):
        x_deg = x_deg -1
    else:
        x_deg = x_deg +1 
    y_deg = 1024 - x_deg
    roller_servo1.goto(x_deg) 
    roller_servo2.goto(y_deg)
    time.sleep_us(1000)
gate_servo.goto(0)
push_servo.goto(500) 

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
        if(feed_mech < -50 and stepper_up == 0):
            print("feed_mech on")
            print("Started Roller")
            roller_pin1.value(1)
            roller_pin2.value(0)
            time.sleep(0.05)
#             gate_servo.goto(350)
            
#             roller_servo1.goto(0) 
#             roller_servo2.goto(1024)
            x_deg = roller_servo1.get_position()
            while x_deg != 0:
                if(x_deg > 0):
                    x_deg = x_deg -1
                else:
                    x_deg = x_deg +1
                y_deg = 1024 - x_deg
                roller_servo1.goto(x_deg) 
                roller_servo2.goto(y_deg)
                time.sleep_us(1000)
        elif(stepper_up == 1):  
#             roller_servo1.goto(312)
#             roller_servo2.goto(712)
            x_deg = roller_servo1.get_position()
            while x_deg != 312:
                if(x_deg > 312):
                    x_deg = x_deg -1
                else:
                    x_deg = x_deg +1 
                y_deg = 1024 - x_deg
                roller_servo1.goto(x_deg) 
                roller_servo2.goto(y_deg)
                time.sleep_us(1000)
        else:
            roller_pin1.value(0)
            roller_pin2.value(0)
            
#             roller_servo1.goto(890)
#             roller_servo2.goto(134)
            
            x_deg = roller_servo1.get_position()
            while x_deg != 890:
                if(x_deg > 890):
                    x_deg = x_deg -1
                else:
                    x_deg = x_deg +1 
                y_deg = 1024 - x_deg
                roller_servo1.goto(x_deg) 
                roller_servo2.goto(y_deg)
                time.sleep_us(1000)
            
            
        if(step_up_down < -80 and stepper_up == 0):
            print("step_up")
#             roller_servo1.goto(312)
#             roller_servo2.goto(712)
            x_deg = roller_servo1.get_position()
            while x_deg != 312:
                if(x_deg > 312):
                    x_deg = x_deg -1
                else:
                    x_deg = x_deg +1 
                y_deg = 1024 - x_deg
                roller_servo1.goto(x_deg) 
                roller_servo2.goto(y_deg)
                time.sleep_us(1000)
            gate_servo.goto(0)
            push_servo.goto(500) 
            stepper_motor.stepper_up(2050)
            stepper_up = 1
        elif(step_up_down > 80 and stepper_up == 1):
            print("step_down")
            gate_servo.goto(0)
            push_servo.goto(500) 
            stepper_motor.stepper_down(2050) 
            stepper_up = 0
    
        if(push_mech > 50):
            print("push_mech on")
            push_servo.goto(1024)
            gate_servo.goto(350) 
        else: 
            push_servo.goto(500)
            gate_servo.goto(0)
    else:
        print("Waiting")
    time.sleep(0.01)











