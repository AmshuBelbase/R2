from machine import Pin
from time import sleep_ms, sleep

step1=Pin(13,Pin.OUT)
dir1=Pin(12,Pin.OUT)
step2=Pin(15,Pin.OUT)
dir2=Pin(14,Pin.OUT)

def stepper_up(steps):
    global step1,step2,dir1,dir2
    dir1.off()
    dir2.off()
    for i in range(steps):
        
        step2.on()
        step1.on()
        sleep_ms(1)
        step2.off()
        step1.off()
        #sleep_ms(1)
        
def stepper_down(steps):
    global step1,step2,dir1,dir2
    
    dir1.on()
    dir2.on()
    for i in range(steps):
        step2.on()
        step1.on()
        sleep_ms(1)
        step2.off()
        step1.off()
        #sleep_ms(1)
    
    

stepper_up(4100)
    
    