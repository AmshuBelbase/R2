# front ultrasonic 
# echo 14
# trig 15 
# left ultrasonic 
# echo 12
# trig 13 
# l298n 
# en1
# in1 
# in2 
# in3 
# in4 
# en2
# en1 21
# in1 20
# in2 19
# in3 18
# in4 17
# en2 16

from machine import Pin, PWM
from BLDC import BLDCMotor
from Ultrasonic import UltrasonicSensor
import time


trigger_F = 15  # Placeholder value, replace with the actual pin number
echo_F = 14  # Placeholder value, replace with the actual pin number
ultraF = UltrasonicSensor(trigger_F, echo_F) 
trigger_L = 12  # Placeholder value, replace with the actual pin number
echo_L = 13  # Placeholder value, replace with the actual pin number
ultraL = UltrasonicSensor(trigger_R, echo_R)
PWM_PIN = 21  # PWM pin for speed control
DIR_PIN1 = 20  # Direction pin 1
DIR_PIN2 = 19  # Direction pin 2
motorL = BLDCMotor(PWM_PIN, DIR_PIN1, DIR_PIN2)
PWM_PIN2 = 16  # PWM pin for speed control
DIR_PIN3 = 18  # Direction pin 1
DIR_PIN4 = 17  # Direction pin 2
motorR = BLDCMotor(PWM_PIN2, DIR_PIN3, DIR_PIN4)

while True:
    dF = ultraF.measure_distance() 
    dL = ultraL.measure_distance()
    if dL>25 and dF>35: #first turn         
        motorL.set_speed(0)
        motorR.set_speed(0) 
    elif dF>35: #just goes forward when the option is available
        if dL > 30:
            motorL.set_speed(50)
            motorR.set_speed(100)
        elif dL < 20:
            motorL.set_speed(100)
            motorR.set_speed(50)
        else:    
            motorL.set_speed(100)
            motorR.set_speed(100) 
    elif dL<25 and dF<35: #first turn         
        motorL.set_speed(100)
        motorR.set_speed(-100)            
    