from machine import Pin
from time import sleep_ms, sleep_us


class StepperMotor:
    def __init__(self, step_pin1, dir_pin1):
        self.step1 = Pin(step_pin1, Pin.OUT)
        self.dir1 = Pin(dir_pin1, Pin.OUT) 

    def stepper_up(self, steps):
        self.dir1.on() 

        for _ in range(steps):
            self.step1.on() 
            sleep_us(500)
            self.step1.off() 
            sleep_us(500)

    def stepper_down(self, steps):
        self.dir1.off() 

        for _ in range(steps):
            self.step1.on() 
            sleep_us(500)
            self.step1.off() 
            sleep_us(500)


