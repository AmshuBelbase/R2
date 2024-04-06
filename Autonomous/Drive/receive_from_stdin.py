# Pico
import sys
import time
import _thread
from machine import Pin

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
            print(data[0], time.time()," received data:- 1: ", data[1], " 2: ", data[2], " 3: ", data[3], " 2: ", data[4])
            data = []
            time.sleep(3)
        time.sleep(0.01)

_thread.start_new_thread(Core1, ())

Core0()
