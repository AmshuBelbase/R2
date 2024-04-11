from machine import Pin 
import time

PWM_PIN = Pin(18, Pin.OUT)  # PWM pin for speed control
DIR_PIN1 = Pin(17, Pin.OUT)  # Direction pin 1
DIR_PIN2 = Pin(16, Pin.OUT)  # Direction pin 2 
PWM_PIN2 = Pin(21, Pin.OUT)  # PWM pin for speed control
DIR_PIN3 = Pin(19, Pin.OUT)  # Direction pin 1
DIR_PIN4 = Pin(20, Pin.OUT)  # Direction pin 2
PWM_PIN.value(1)
PWM_PIN2.value(1)
while True: 
    print("Forward")
    DIR_PIN1.off()
    DIR_PIN2.on()
    DIR_PIN3.on()
    DIR_PIN4.off()
    time.sleep(1) 