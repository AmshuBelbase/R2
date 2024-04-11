from machine import Pin, PWM
from BLDC import BLDCMotor
from Ultrasonic import UltrasonicSensor
import time



trigger_F = 15  # Placeholder value, replace with the actual pin number
echo_F = 14  # Placeholder value, replace with the actual pin number
ultraF = UltrasonicSensor(trigger_F, echo_F) 
trigger_L = 9  # Placeholder value, replace with the actual pin number
echo_L = 8  # Placeholder value, replace with the actual pin number
ultraL = UltrasonicSensor(trigger_L, echo_L)

PWM_PIN = PWM(Pin(18))  # PWM pin for speed control
DIR_PIN1 = Pin(16, Pin.OUT)  # Direction pin 1
DIR_PIN2 = Pin(17, Pin.OUT)  # Direction pin 2 
PWM_PIN2 = PWM(Pin(21))  # PWM pin for speed control
DIR_PIN3 = Pin(19, Pin.OUT)  # Direction pin 1
DIR_PIN4 = Pin(20, Pin.OUT)  # Direction pin 2 

 
PWM_PIN = 18  # PWM pin for speed control
DIR_PIN1 = 17  # Direction pin 1
DIR_PIN2 = 16  # Direction pin 2
motorL = BLDCMotor(PWM_PIN, DIR_PIN1, DIR_PIN2)
PWM_PIN2 = 21  # PWM pin for speed control
DIR_PIN3 = 19  # Direction pin 1
DIR_PIN4 = 20  # Direction pin 2
motorR = BLDCMotor(PWM_PIN2, DIR_PIN3, DIR_PIN4)
hardcode = 0

while True: 
    dF = ultraF.measure_distance()  
    dL = ultraL.measure_distance() 
    if dL>35 and dF>35:
        print("Stop")
        motorL.set_speed(0)
        motorR.set_speed(0)
    elif dF>35: 
        if dL > 25:
            print("Forward - Left")
            motorL.set_speed(80)
            motorR.set_speed(100)
        elif dL < 10:
            print("Forward - Right")
            motorL.set_speed(100)
            motorR.set_speed(80)
        else:    
            print("Forward")
            motorL.set_speed(100)
            motorR.set_speed(100) 
    elif dL<25 and dF<35: #first turn
        print("Right Turn")
        motorL.set_speed(100)
        motorR.set_speed(-100) 