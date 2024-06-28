from machine import I2C
from hmc5883l import HMC5883L
from time import sleep

from machine import Pin, PWM, UART 
import sys
from sys import stdin
import time
import _thread
import uselect

m1_pwm = PWM(Pin(4))
m1_dir = Pin(14, Pin.OUT)
m2_pwm = PWM(Pin(16))
m2_dir = Pin(28, Pin.OUT)
m3_pwm = PWM(Pin(17))
m3_dir = Pin(10, Pin.OUT)
m4_pwm = PWM(Pin(5))
m4_dir = Pin(6, Pin.OUT)


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
        
        
sensor = HMC5883L()

Xmin=1000
Xmax=-1000
Ymin=1000
Ymax=-1000

x_con = ""
y_con = ""

slow_us = 4000
drive(-slow_us,slow_us,-slow_us,slow_us)

while True:
    try:
        sleep(0.2)
        x, y, z = sensor.read()
        x_con += " | "+str(x)
        y_con += " | "+str(y)
        Xmin=min(x,Xmin)
        Xmax=max(x,Xmax)
        Ymin=min(y,Ymin)
        Ymax=max(y,Ymax)
        print(sensor.format_result(x, y, z))
        print("Xmin="+str(Xmin)+"; Xmax="+str(Xmax)+"; Ymin="+str(Ymin)+"; Ymax="+str(Ymax))

    except KeyboardInterrupt:
        print()
        print('Got ctrl-c')
        print(x_con)
        print(y_con)
        xs=1
        ys=(Xmax-Xmin)/(Ymax-Ymin)
        xb =xs*(1/2*(Xmax-Xmin)-Xmax)
        yb =xs*(1/2*(Ymax-Ymin)-Ymax)
        print("Calibration corrections:")
        print("xs="+str(xs))
        print("xb="+str(xb))
        print("ys="+str(ys))
        print("yb="+str(yb))
        break