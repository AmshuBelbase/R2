from machine import Pin
from time import sleep_ms, sleep

step1 = Pin(13, Pin.OUT)
dir1 = Pin(12, Pin.OUT)

step2 = Pin(15, Pin.OUT)
dir2 = Pin(14, Pin.OUT)

def stepper_up(steps):
    dir1.off()
    dir2.off() 
    for _ in range(steps):
        step1.on()
        step2.on()
        sleep_ms(1)
        step1.off()
        step2.off()
        sleep_ms(1)
        
def stepper_down(steps):
    dir1.on()
    dir2.on()
    
    for _ in range(steps):
        step1.on()
        step2.on()
        sleep_ms(1)
        step1.off()
        step2.off()
        sleep_ms(1)

while True:
    stepper_down(1000)
    print("Stepping")
    sleep(0.2)