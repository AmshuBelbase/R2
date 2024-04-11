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
trigger_L = 13  # Placeholder value, replace with the actual pin number
echo_L = 12  # Placeholder value, replace with the actual pin number
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
    dR = ultraR.measure_distance()
    dL = ultraL.measure_distance()
    if dF>35: #just goes forward when the option is available
        while dF>35:
            motorL.set_speed(100)
            motorR.set_speed(100)
            dF = ultraF.measure_distance()
            dR = ultraR.measure_distance()
            dL = ultraL.measure_distance()
    if dL<25 and dF<35: #first turn
        
        dL = ultraL.measure_distance()
        
        motorL.set_speed(-100)
        motorR.set_speed(100)
        time.sleep(0.3)
        while dF<100 and ultraL.measure_distance()!=dL:
            #goes right 
            
            dF = ultraF.measure_distance()
            dR = ultraR.measure_distance()
    if dL>25 and dF<80: #final turn
        while dF<80:
            #goes left
            motorL.set_speed(100)
            motorR.set_speed(-100)
            dF = ultraF.measure_distance()
            dR = ultraR.measure_distance()
            dL = ultraL.measure_distance()            
    