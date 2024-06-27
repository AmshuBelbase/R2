# R2 Pico - DRIVE
from machine import Pin, PWM, UART 
import sys
import time
import _thread
import uselect

# ----------------- PINOUTS ----------------- 

m1_pwm = PWM(Pin(4))
m1_dir = Pin(14, Pin.OUT)
m2_pwm = PWM(Pin(16))
m2_dir = Pin(28, Pin.OUT)
m3_pwm = PWM(Pin(17))
m3_dir = Pin(10, Pin.OUT)
m4_pwm = PWM(Pin(5))
m4_dir = Pin(6, Pin.OUT) 

left_back_trig = Pin(2, Pin.OUT) #us1
left_back_echo = Pin(3, Pin.IN)

left_front_trig = Pin(21, Pin.OUT) #us2
left_front_echo = Pin(7, Pin.IN)

front_left_trig = Pin(18, Pin.OUT) #us3  
front_left_echo = Pin(11, Pin.IN)

front_right_trig = Pin(20, Pin.OUT) #us4
front_right_echo = Pin(15, Pin.IN)

# right_front_trig = Pin(19, Pin.OUT) #us5
# right_front_echo = Pin(27, Pin.IN)

led_pin = Pin(25, Pin.OUT)
led_pin.value(0)

uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))

# ----------------- USER DEFINED FUNCTIONS -----------------

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
         

def measure_distance(trigger, echo):
    
    trigger.off()
    time.sleep_us(2)
    trigger.on()
    time.sleep_us(10)
    trigger.off()
 
    while echo.value() == 0:
        pass
    start_time = time.ticks_us()
 
    while echo.value() == 1:
        pass
    end_time = time.ticks_us()
 
    duration = time.ticks_diff(end_time, start_time)
 
    distance = duration * 34300 / (2 * 1000000)  # Convert microseconds to seconds

    return distance
print("Warming Up")
drive(0,0,0,0)

i = 1
time_s = 3
led_pin.value(0)
while i<=time_s:
    i=i+1
    led_pin.value(1)
    time.sleep_ms(500)
    led_pin.value(0)
    time.sleep_ms(500)
led_pin.value(1)

print("Started")
slow = 4500
medium = 9000
fast = 24000
super_fast = 36000
d = 18000

garbage_c = 0
forward_c = 0
    
while True:
        print("loop")
        
        front_left_us = measure_distance(front_left_trig, front_left_echo) 
        print("Front Left: ", front_left_us)        
        time.sleep_ms(1)

        left_front_us = measure_distance(left_front_trig, left_front_echo)  
        print("Left Front: ", left_front_us)
        time.sleep_ms(1)

        left_back_us = measure_distance(left_back_trig, left_back_echo)  
        print("Left Back: ", left_back_us)
        time.sleep_ms(1)

#         right_front_us = measure_distance(right_front_trig, right_front_echo)  
#         print("Right Front: ", right_front_us)
#         time.sleep_ms(1)
        
        front_right_us = measure_distance(front_right_trig, front_right_echo)
        print("Front Right: ", front_right_us)
        time.sleep_ms(1)       
        
        if(front_left_us <=140 and front_right_us <= 140):
            d = medium
        else:
            d = fast
            
        if(front_left_us <= 55 and front_right_us <= 55):
            if(abs(front_left_us-front_right_us) >= 3):
                if(front_left_us > front_right_us):
                    print("Clockwise 1")
                    drive(slow,-slow,slow,-slow)
                else:
                    print("Anti Clockwise 1")
                    drive(-slow,slow,-slow,slow)
            elif(front_left_us <= 10 and front_right_us <= 10): 
                print("Back")
                drive(0,slow,0,-slow)
            elif(front_left_us <= 20 and front_right_us <= 20): #and right_front_us > 160
                print("Move Right 1")
                drive(fast,0,-fast,0)
            else:
                print("Front")
                drive(0,-slow,0,slow)
        elif(left_front_us <= 65 and left_back_us <= 65):
            if(abs(left_front_us-left_back_us) >= 4):
                if(left_back_us > left_front_us):
                    print("Clockwise 2")
                    drive(slow,-slow,slow,-slow)
                else:
                    print("Anti Clockwise 2")
                    drive(-slow,slow,-slow,slow)
            elif(left_front_us <= 10 and left_back_us <= 10):
                print("Diagonal Front Right 2")
                drive(slow,-slow,-slow,slow)
            elif(left_front_us <= 27 and left_back_us <= 27):
                print("Straight 2")
                drive(0,-d,0,d)
            else:
                print("Diagonal Front Left 2")
                drive(-slow,-slow,slow,slow)
#         elif(right_front_us >=118 and right_front_us <=128):
#             print("Stop 0")
#             drive(0,0,0,0)
#             forward_c += 1
#             print("forward_c:",forward_c)
#             if(forward_c >= 2):
#                 print("Moving straight for 2.5 seconds 3")
#                 drive(0,-super_fast,0,super_fast)
#                 time.sleep_ms(1750)
#                 print("Anticlockwise for 1 seconds 3")
#                 drive(-medium,medium,-medium,medium)
#                 time.sleep_ms(500)
#                 print("Stop 3")
#                 drive(0,0,0,0)
#                 drive_stat = 1 #1
#                 break 
#         elif(right_front_us <128):
#             print("Move Left 2")
#             drive(-slow,0,slow,0)
#         elif(right_front_us <= 160):
#             print("Moving right 5")
#             drive(slow,0,-slow,0)
        elif(front_right_us > 45 and front_left_us < 45):
            print("Moving right 6")
            drive(slow,0,-slow,0)
        elif(front_left_us >= 45 and front_right_us >= 45):
            print("Stop 3") 
            drive(0,0,0,0)
            forward_c += 1
            print("forward_c:",forward_c)
            if(forward_c >= 5):
                print("Moving right for 0.3 seconds 3")
                drive(medium,0,-medium,0)
                time.sleep(0.3)
                print("Moving straight for 2 seconds 3")
                drive(0,-super_fast,0,super_fast)
                time.sleep(2)
                print("Anticlockwise for 0.8 seconds 3")
                drive(-medium,medium,-medium,medium)
                time.sleep_ms(800) 
                drive(0,-medium,0,medium)
                time.sleep(2)
                print("Stop 3") 
                drive(0,0,0,0)
                drive_stat = 1 #1
                break 
        else:
            print("Stop - Confused 7")
            drive(0,0,0,0)
            garbage_c += 1
            print("garbage_c:",garbage_c) 
        time.sleep_ms(2)
