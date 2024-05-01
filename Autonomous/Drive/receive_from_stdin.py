# Pico
import sys
import time
import _thread
from machine import Pin
print("Started")
led = Pin(25, Pin.OUT)

data = []


def Core0():
    global data
    while True:
        buf = sys.stdin.readline().rstrip('\n')
        try:
            data = [int(i) for i in buf.split('|')]
            if (data[0] % 1000 == 0):
                led.on()
            else:
                led.off()
        except ValueError:
            print("Non-integer detected.")
            continue


def Core1():
    global data
    while True:
        if(data!=[]):
            print(" received data:- 1: ", data[0], " 2: ", data[1], " 3: ", data[2], " 4: ", data[3])
            data = []
#             time.sleep(3) 

_thread.start_new_thread(Core1, ())

Core0()
