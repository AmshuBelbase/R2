from machine import Pin
from time import sleep_ms

class StepperMotor:
    def __init__(self, step_pin1, dir_pin1, step_pin2, dir_pin2):
        self.step1 = Pin(step_pin1, Pin.OUT)
        self.dir1 = Pin(dir_pin1, Pin.OUT)
        self.step2 = Pin(step_pin2, Pin.OUT)
        self.dir2 = Pin(dir_pin2, Pin.OUT)

    def stepper_up(self, steps):
        self.dir1.off()
        self.dir2.off()
        
        for _ in range(steps):
            self.step1.on()
            self.step2.on()
            sleep_ms(1)
            self.step1.off()
            self.step2.off()
            #sleep_ms(1)
            
    def stepper_down(self, steps):
        self.dir1.on()
        self.dir2.on()
        
        for _ in range(steps):
            self.step1.on()
            self.step2.on()
            sleep_ms(1)
            self.step1.off()
            self.step2.off()
            #sleep_ms(1)

