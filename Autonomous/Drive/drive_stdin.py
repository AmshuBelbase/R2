# Pico
import sys
import time
import _thread 
from machine import Pin, PWM, UART 
import utime

m1_pwm = PWM(Pin(7))
m1_dir = Pin(3, Pin.OUT)
m2_pwm = PWM(Pin(6))
m2_dir = Pin(2, Pin.OUT)
m3_pwm = PWM(Pin(21))
m3_dir = Pin(27, Pin.OUT)
m4_pwm = PWM(Pin(20))
m4_dir = Pin(26, Pin.OUT)
 
mech_pico_signal_pin = Pin(14, Pin.OUT)

data = []


# Function to convert the values
def map(val, loval, hival, tolow, tohigh):
    return (val - loval) / (hival - loval) * (tohigh - tolow) + tolow


def drive(speed1, speed2, speed3, speed4):

    m1_pwm.freq(100)
    if speed1 < 0:
        m1_dir.value(0)
        m1_pwm.duty_u16(abs(speed1))  # absolute speed
    elif speed1 > 0:
        m1_dir.value(1)
        m1_pwm.duty_u16(speed1)
    else:
        m1_pwm.duty_u16(0)

    m2_pwm.freq(100)
    if speed2 < 0:
        m2_dir.value(0)
        m2_pwm.duty_u16(abs(speed2))  # absolute speed
    elif speed2 > 0:
        m2_dir.value(1)
        m2_pwm.duty_u16(speed2)
    else:
        m2_pwm.duty_u16(0)

    m3_pwm.freq(100)
    if speed3 < 0:
        m3_dir.value(0)
        m3_pwm.duty_u16(abs(speed3))  # absolute speed
    elif speed3 > 0:
        m3_dir.value(1)
        m3_pwm.duty_u16(speed3)
    else:
        m3_pwm.duty_u16(0)

    m4_pwm.freq(100)
    if speed4 < 0:
        m4_dir.value(0)
        m4_pwm.duty_u16(abs(speed4))  # absolute speed
    elif speed4 > 0:
        m4_dir.value(1)
        m4_pwm.duty_u16(speed4)
    else:
        m4_pwm.duty_u16(0)


def calc_motor_speed(vx, vy, omega):
    w1 = int(15.75 * vx + (-5.66909078166105) * omega)
    w2 = int(0 + 15.75 * vy + 5.66909078166105 * omega)
    w3 = int((-15.75) * vx + 0 + 5.66909078166105 * omega)
    w4 = int(0 + (-15.75) * vy + (-5.66909078166105) * omega)

    # print(w1)
    # print(w2)
    # print(w3)
    # print(w4)
    # Return motor speeds
    return w1, w2, w3, w4



def Core0():
    global data
    while True:
        buf = sys.stdin.readline().rstrip('\n')
        try:
            data = [int(i) for i in buf.split('|')] 
        except ValueError:
            print("Non-integer detected.")
            continue


def Core1():
    global data
    while True:
        if(data==[]):
            drive(0, 0, 0, 0)
#             print("Data has not Arrived")
        elif(data!=[]):    
            print(data[0], time.time()," received data:- 1: ", data[1], " 2: ", data[2], " 3: ", data[3], " 2: ", data[4])
            if(data[2] > 255 or data[2] < -255 or data[1] > 255 or data[1] < -255 or data[3] > 255 or data[3] < -255 or data[4] > 255 or data[4] < -255):
               print("Invalid Data received")
            else:   
                wm1 = int(map(data[1], -255, 255, -19660, 19660))
                wm2 = int(map(data[2], -255, 255, -19660, 19660))
                wm3 = int(map(data[3], -255, 255, -19660, 19660))
                wm4 = int(map(data[4], -255, 255, -19660, 19660))
                drive(wm1, wm2, wm3, wm4) 
                print(data[0]," W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))
                utime.sleep_ms(10)
            data = []
#             time.sleep(3)
        time.sleep(0.01)

_thread.start_new_thread(Core1, ())

Core0()