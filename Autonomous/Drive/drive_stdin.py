from machine import Pin, PWM, UART 
import utime
import time
import sys 
import _thread

print("Started")
led = Pin(25, Pin.OUT)

data = []


m1_pwm = PWM(Pin(7))
m1_dir = Pin(3, Pin.OUT)
m2_pwm = PWM(Pin(6))
m2_dir = Pin(2, Pin.OUT)
m3_pwm = PWM(Pin(21))
m3_dir = Pin(27, Pin.OUT)
m4_pwm = PWM(Pin(20))
m4_dir = Pin(26, Pin.OUT)


uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))


def map(val, loval, hival, tolow, tohigh):
    return (val - loval) / (hival - loval) * (tohigh - tolow) + tolow


def drive(speed1, speed2, speed3, speed4):
    m1_pwm.freq(9000)
    if speed1 < 0:
        m1_dir.value(0)
        m1_pwm.duty_u16(abs(speed1))  # absolute speed
    elif speed1 > 0:
        m1_dir.value(1)
        m1_pwm.duty_u16(speed1)
    else:
        m1_pwm.duty_u16(0)

    m2_pwm.freq(9000)
    if speed2 < 0:
        m2_dir.value(0)
        m2_pwm.duty_u16(abs(speed2))  # absolute speed
    elif speed2 > 0:
        m2_dir.value(1)
        m2_pwm.duty_u16(speed2)
    else:
        m2_pwm.duty_u16(0)

    m3_pwm.freq(9000)
    if speed3 < 0:
        m3_dir.value(0)
        m3_pwm.duty_u16(abs(speed3))  # absolute speed
    elif speed3 > 0:
        m3_dir.value(1)
        m3_pwm.duty_u16(speed3)
    else:
        m3_pwm.duty_u16(0)

    m4_pwm.freq(9000)
    if speed4 < 0:
        m4_dir.value(0)
        m4_pwm.duty_u16(abs(speed4))  # absolute speed
    elif speed4 > 0:
        m4_dir.value(1)
        m4_pwm.duty_u16(speed4)
    else:
        m4_pwm.duty_u16(0)

 
def Core0():
    global data
    print("In core0")
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
    print("In core1")
    while True: 
        if(data!=[]):            
            print(" received data:- 1: ", data[0], " 2: ", data[1], " 3: ", data[2], " 4: ", data[3])
            wm1 = int(map(data[0], -255, 255, -50000, 50000))
            wm2 = int(map(data[1], -255, 255, -50000, 50000))
            wm3 = int(map(data[2], -255, 255, -50000, 50000))
            wm4 = int(map(data[3], -255, 255, -50000, 50000))
            print("After Mapping")
            print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))
            drive(wm1*-1, wm2*1, wm3*-1, wm4*1)
        else:
            drive(0,0,0,0)
        utime.sleep_ms(30)
        data = [] 
         

_thread.start_new_thread(Core1, ())

Core0()
