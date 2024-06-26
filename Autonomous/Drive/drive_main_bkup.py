# R2 Pico - DRIVE
from machine import Pin, PWM, UART 
import sys
import time
import _thread 

# ----------------- PINOUTS -----------------

m1_pwm = PWM(Pin(4))
m1_dir = Pin(14, Pin.OUT)
m2_pwm = PWM(Pin(16))
m2_dir = Pin(28, Pin.OUT)
m3_pwm = PWM(Pin(17))
m3_dir = Pin(10, Pin.OUT)
m4_pwm = PWM(Pin(5))
m4_dir = Pin(6, Pin.OUT) 

front_left_trig = Pin(18, Pin.OUT) #us3  
front_left_echo = Pin(11, Pin.IN)

front_right_trig = Pin(20, Pin.OUT) #us4
front_right_echo = Pin(15, Pin.IN)

left_front_trig = Pin(21, Pin.OUT) #us2
left_front_echo = Pin(7, Pin.IN)

left_back_trig = Pin(2, Pin.OUT) #us1
left_back_echo = Pin(3, Pin.IN)

right_front_trig = Pin(19, Pin.OUT) #us5
right_front_echo = Pin(27, Pin.IN)

led_pin = Pin(25, Pin.OUT)
led_pin.value(0)

uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))

# ----------------- GLOBAL AVRIABLES -----------------

data = []
drive_stat = 0 # donot listen to laptop

slow = 5000
medium = 9000
fast = 24000
super_fast = 36000
d = 18000



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
    # Send a 10us pulse to trigger the sensor
    trigger.off()
    time.sleep_us(2)
    trigger.on()
    time.sleep_us(10)
    trigger.off()

    # Wait for the echo to start
    while echo.value() == 0:
        pass
    start_time = time.ticks_us()

    # Wait for the echo to end
    while echo.value() == 1:
        pass
    end_time = time.ticks_us()

    # Calculate the duration of the echo pulse
    duration = time.ticks_diff(end_time, start_time)

    # Convert the duration to distance (in cm)
    # Speed of sound = 343 m/s = 34300 cm/s
    # Distance = (duration * speed of sound) / 2
    distance = duration * 34300 / (2 * 1000000)  # Convert microseconds to seconds

    return distance

# ----------------- INITIAL POSITIONS -----------------

print("Started")
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

while False:
    left_back_us = measure_distance(left_back_trig, left_back_echo)  
    print("Left Back: ", left_back_us)
    
    print("loop")
    front_left_us = measure_distance(front_left_trig, front_left_echo) 
    print("Front Left: ", front_left_us)

    left_front_us = measure_distance(left_front_trig, left_front_echo)  
    print("Left Front: ", left_front_us) 

    right_front_us = measure_distance(right_front_trig, right_front_echo)  
    print("Right Front: ", right_front_us)
    
    front_right_us = measure_distance(front_right_trig, front_right_echo)
    print("Front Right: ", front_right_us)

    time.sleep_ms(10)


def Core0():
    global data
    while True:
        buf = sys.stdin.readline().rstrip('\n')
        print("Buffer: ",buf)
        try:
            data = [int(i) for i in buf.split('|')]
#             if (data[0] % 1000 == 0):
#                 led_pin.value(1)
#             else:
#                 led_pin.value(0)
        except ValueError:
            print("Non-integer detected.")
            continue


def Core1():
    global data
    global drive_stat
    global slow, medium, fast, super_fast
    garbage_c = 0
    forward_c = 0
    drive_stat = 0
    message = "{}".format(drive_stat)
    print(message)
    message_bytes = message.encode('utf-8')
    uart.write(message_bytes)
    time.sleep_ms(5)

    while False:
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

        right_front_us = measure_distance(right_front_trig, right_front_echo)  
        print("Right Front: ", right_front_us)
        time.sleep_ms(1)
        
        front_right_us = measure_distance(front_right_trig, front_right_echo)
        print("Front Right: ", front_right_us)
        time.sleep_ms(1)       
        
        if(front_left_us <=140 and front_right_us <= 140):
            d = medium # 7000
        else:
            d = fast # 18000
#         if(front_left_us <= 45 and front_right_us <= 45 and right_front_us <128 and left_front_us > 45 and left_back_us > 45):
#             print("Move Left 1")
#             drive(-slow,0,slow,0) # 4000
        if(front_left_us <= 45 and front_right_us <= 45):
            if(abs(front_left_us-front_right_us) >= 3):
                if(front_left_us > front_right_us):
                    print("Clockwise 1")
                    drive(slow,-slow,slow,-slow) # 2500
                else:
                    print("Anti Clockwise 1")
                    drive(-slow,slow,-slow,slow) # 2500
            elif(front_left_us <= 10 and front_right_us <= 10):
#                 print("Digonal Back Right 1")
#                 drive(slow,slow,-slow,-slow) # 3000
                print("Back")
                drive(0,slow,0,-slow)
            elif(front_left_us <= 20 and front_right_us <= 20): #and right_front_us > 160
                print("Move Right 1")
                drive(fast,0,-fast,0) #18000
            else:
#                 print("Diagonal Front Right 1")
#                 drive(-slow,-slow,slow,slow) # 3000
                print("Front")
                drive(0,-slow,0,slow)
        elif(left_front_us <= 40 and left_back_us <= 40):
            if(abs(left_front_us-left_back_us) >= 4):
                if(left_back_us > left_front_us):
                    print("Clockwise 2")
                    drive(slow,-slow,slow,-slow) # 2500
                else:
                    print("Anti Clockwise 2")
                    drive(-slow,slow,-slow,slow)  # 2500
            elif(left_front_us <= 10 and left_back_us <= 10):
                print("Diagonal Front Right 2")
                drive(slow,-slow,-slow,slow) # 5000
            elif(left_front_us <= 27 and left_back_us <= 27):
                print("Straight 2")
                drive(0,-d,0,d)
            else:
                print("Diagonal Front Left 2")
                drive(-slow,-slow,slow,slow) #5000
        elif(right_front_us >=118 and right_front_us <=128):
            print("Stop 0")
            drive(0,0,0,0)
            forward_c += 1
            print("forward_c:",forward_c)
            if(forward_c >= 2):
                print("Moving straight for 2.5 seconds 3")
                drive(0,-super_fast,0,super_fast) # 30000
                time.sleep_ms(1750)
                print("Anticlockwise for 1 seconds 3")
                drive(-medium,medium,-medium,medium) #10000
                time.sleep_ms(500)
                print("Stop 3")
                drive(0,0,0,0)
                drive_stat = 1 #1
                break 
        elif(right_front_us <128):
            print("Move Left 2")
            drive(-slow,0,slow,0) # 4000
        elif(right_front_us <= 160):
            print("Moving right 5")
            drive(slow,0,-slow,0) # 4000
        elif(front_right_us > 45 and front_left_us < 45):
            print("Moving right 6")
            drive(slow,0,-slow,0) # 4000
        else:
            print("Stop - Confused 7")
            drive(0,0,0,0)
            garbage_c += 1
            print("garbage_c:",garbage_c)
            if(garbage_c >= 2):
                break  
        time.sleep_ms(2)
        
    drive_stat = 1
    message = "{}".format(drive_stat)
    print(message)
    message_bytes = message.encode('utf-8')
    uart.write(message_bytes)
    
    while True:
        if uart.any():
            print("received")
            message_bytes = uart.read()
            message = message_bytes.decode('utf-8')
            li = list(message.split(","))
            if(len(li) == 1): 
                drive_stat = int(li[0])
            else:
                continue
        if(data!=[] and drive_stat == 1):
            print(" received data:- 1: ", data[0], " 2: ", data[1], " 3: ", data[2], " 4: ", data[3]) 
            wm1 = int(map(data[0], -255, 255, -50000, 50000))
            wm2 = int(map(data[1], -255, 255, -50000, 50000))
            wm3 = int(map(data[2], -255, 255, -50000, 50000))
            wm4 = int(map(data[3], -255, 255, -50000, 50000))
#             print("After Mapping")
#             print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))
            drive(wm1*-1, wm2*1, wm3*-1, wm4*1) 
            time.sleep_ms(30)
#         data = [] 
        if(drive_stat == 0):
#             print("Drive Stop")
            drive(0,0,0,0)
        if(drive_stat == 2):
            print("Adjust according to Mech pico.")

_thread.start_new_thread(Core1, ())

Core0()
