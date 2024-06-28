# R2 Pico - DRIVE
from machine import Pin, PWM, UART 
import sys
from sys import stdin
import time
import _thread
import uselect

from machine import I2C
from hmc5883l import HMC5883L
from time import sleep

# ----------------- PINOUTS -----------------

#magnetometer  - 8 sda and 9 scl (mechanisms)

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


def save_to_csv(data): 
  with open(csv_filename, "a") as f: 
    f.write(data + "\n")
    
def clear_csv(data): 
  with open(csv_filename, "w") as f: 
    f.write(data + "\n")



# ----------------- GLOBAL AVRIABLES -----------------

data = []  

drive_stat = 0
right_move = 1

slow = 3500
medium = 8000
fast = 20000
fast_med = 16000
super_fast = 36000
# d = 18000

slow_us = 4500
medium_us = 9000
fast_us = 24000
super_fast_us = 36000
d = 18000

garbage_c = 0
forward_c = 0

csv_filename = "us_data.csv"
clear_csv(" ")

sensor = HMC5883L()
x, y, z = sensor.read()
deg = sensor.get_degree(x, y, z)

count=0
range_min = 265
range_max = 275


# ----------------- INITIAL POSITIONS -----------------

save_to_csv(" ------------------- NEW ATTEMPT -------------------")
# print("Warming Up")
save_to_csv("Warming Up")
drive(0,0,0,0)

i = 1
time_s = 1     
led_pin.value(0)
while i<=time_s:
    i=i+1
    led_pin.value(1)
    time.sleep_ms(500)
    led_pin.value(0)
    time.sleep_ms(500)
led_pin.value(1)

# print("Started")
save_to_csv("Started")

# ----------------- READ ULTRASONICS -----------------

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
    
#     front_right_us = measure_distance(front_right_trig, front_right_echo)
#     print("Front Right: ", front_right_us)

    time.sleep_ms(10)
    


# ----------------- MAIN CODE -----------------
us_data = ''
while drive_stat == 0:
    buffer = ''  
    select_result = uselect.select([stdin], [], [], 0)
    while select_result[0]:
        input_character = stdin.read(1)
        if input_character != '#':
            buffer += input_character
        else:
            try:
                data = [int(i) for i in buffer.split('|')]
#                 print(data)
                us_data = us_data + f" | data: "  + str(data)
            except ValueError:
#                 print("Non-integer detected.")
                us_data = us_data + f" | Non-integer detected"
                continue 
            buffer = ''
        select_result = uselect.select([stdin], [], [], 0)
        
    if uart.any():
#         print("received")
        message_bytes = uart.read()
        message = message_bytes.decode('utf-8') 
        us_data = us_data + " | received: " + str(message)
        li = list(message.split(","))
        if(len(li) == 1): 
            drive_stat = int(li[0])
        else:
            continue
#         print(drive_stat)
        us_data = us_data + " | Drive Stat: " + str(drive_stat)


message = "{}".format(drive_stat)
# print(message)
us_data += f" | message: " + str(message)
message_bytes = message.encode('utf-8')
uart.write(message_bytes)
time.sleep_ms(5)
save_to_csv(" ------------------- AREA 1 TO AREA 3 -------------------")
save_to_csv(us_data)

while True:
#     print("loop")
    
    front_left_us = measure_distance(front_left_trig, front_left_echo) 
#     print("Front Left: ", front_left_us)        
    time.sleep_ms(1)

    left_front_us = measure_distance(left_front_trig, left_front_echo)  
#     print("Left Front: ", left_front_us)
    time.sleep_ms(1)

    left_back_us = measure_distance(left_back_trig, left_back_echo)  
#     print("Left Back: ", left_back_us)
    time.sleep_ms(1)

#         right_front_us = measure_distance(right_front_trig, right_front_echo)  
#         print("Right Front: ", right_front_us)
#         time.sleep_ms(1)
    
    front_right_us = measure_distance(front_right_trig, front_right_echo)
#     print("Front Right: ", front_right_us)
    time.sleep_ms(1)       
    
    if(front_left_us <=140 and front_right_us <= 140):
        d = medium_us
    else:
        d = fast_us
        
    if(front_left_us <= 55 and front_right_us <= 55):
        if(abs(front_left_us-front_right_us) >= 3):
            if(front_left_us > front_right_us):
#                 print("Clockwise 1")
                drive(slow_us,-slow_us,slow_us,-slow_us)
            else:
#                 print("Anti Clockwise 1")
                drive(-slow_us,slow_us,-slow_us,slow_us)
        elif(front_left_us <= 10 and front_right_us <= 10): 
#             print("Back")
            drive(0,slow_us,0,-slow_us)
        elif(front_left_us <= 17 and front_right_us <= 17): #and right_front_us > 160
#             print("Move Right 1")
            drive(fast_us,0,-fast_us,0)
        else:
#             print("Front")
            drive(0,-slow_us,0,slow_us)
    elif(left_front_us <= 65 and left_back_us <= 65):
        if(abs(left_front_us-left_back_us) >= 4):
            if(left_back_us > left_front_us):
#                 print("Clockwise 2")
                drive(slow_us,-slow_us,slow_us,-slow_us)
            else:
#                 print("Anti Clockwise 2")
                drive(-slow_us,slow_us,-slow_us,slow_us)
        elif(left_front_us <= 10 and left_back_us <= 10):
#             print("Diagonal Front Right 2")
            drive(medium_us,-medium_us,-medium_us,medium_us)
        elif(left_front_us <= 27 and left_back_us <= 27):
#             print("Straight 2")
            drive(0,-d,0,d)
        else:
#             print("Diagonal Front Left 2")
            drive(-medium_us,-medium_us,medium_us,medium_us)
#         elif(right_front_us >=118 and right_front_us <=128):
#             print("Stop 0")
#             drive(0,0,0,0)
#             forward_c += 1
#             print("forward_c:",forward_c)
#             if(forward_c >= 2):
#                 print("Moving straight for 2.5 seconds 3")
#                 drive(0,-super_fast_us,0,super_fast_us)
#                 time.sleep_ms(1750)
#                 print("Anticlockwise for 1 seconds 3")
#                 drive(-medium_us,medium_us,-medium_us,medium_us)
#                 time.sleep_ms(500)
#                 print("Stop 3")
#                 drive(0,0,0,0)
#                 drive_stat = 1 #1
#                 break 
#         elif(right_front_us <128):
#             print("Move Left 2")
#             drive(-slow_us,0,slow_us,0)
#         elif(right_front_us <= 160):
#             print("Moving right 5")
#             drive(slow_us,0,-slow_us,0)
    elif(front_right_us > 45 and front_left_us < 45):
#         print("Moving right 6")
        drive(slow_us,0,-slow_us,0)
    elif(front_left_us >= 45 and front_right_us >= 45):
#         print("Stop 3") 
        drive(0,0,0,0)
        forward_c += 1
#         print("forward_c:",forward_c)
        if(forward_c >= 5):
#             print("Moving right for 0.3 seconds 3")
            drive(medium_us,0,-medium_us,0)
            time.sleep(0.3)
#             print("Moving straight for 2 seconds 3")
            drive(0,-super_fast_us,0,super_fast_us)
            time.sleep(2)
#             print("Anticlockwise for 0.8 seconds 3")
            drive(-medium_us,medium_us,-medium_us,medium_us)
            time.sleep_ms(800) 
            drive(0,-fast_us,0,fast_us)
            time.sleep(1.2)
#             print("Stop 3") 
            drive(0,0,0,0)
            drive_stat = 1 #1
            break 
    else:
#         print("Stop - Confused 7")
        drive(0,0,0,0)
        garbage_c += 1
#         print("garbage_c:",garbage_c) 
    time.sleep_ms(2)

us_data = ''
message = "{}".format(drive_stat)
us_data = us_data + " | message: " + str(message)
# print(message)
message = f"{drive_stat}\n"
# Send the message over USB CDC (print to USB)
print(message, end='')
message_bytes = message.encode('utf-8')
uart.write(message_bytes)

save_to_csv(" ------------------- INSIDE AREA 3 -------------------")

ranges_silo = [
    (0,250, 20),
    (0,500, 15),
    (0, 1000, 8),
    (0, 2000, 5), 
    (0, 4000, 2),
    (0, 5000, 1.2) 
]
# ranges = [
#     (0, 1000, 3),
#     (1000, 2000, 2), 
#     (2000, 4000, 1.5),
#     (4000, 5000, 1.2),
#     (5000, 10000, 0.5),
#     (10000, 20000, 0.35),
#     (20000, 62000, 0.3)
# ]
ranges = [
    (0, 1000, 3),
    (1000, 2000, 2), 
    (2000, 4000, 1.5),
    (4000, 5000, 1.2),
    (5000, 10000, 0.75),
    (10000, 20000, 0.5),
    (20000, 62000, 0.4)
]

# ----------------- DRIVE STATUS -----------------

# drive_stat = 0  | STOP 
# drive_stat = 1  | FOLLOW LAPTOP, STOP ROLLER AT 500, GATE CLOSED
# drive_stat = 2  | BALL IN RANGE, GO BACK, OPEN ROLLER AT 180, GO FRONT
# drive_stat = 3  | FEED BALL
# drive_stat = 4  | FEED BALL, DISCARD, drive_stat = 1
# drive_stat = 5  | GO BACK FOR EASIER FEED
# drive_stat = 6  | SEARCH SILOS
# drive_stat = 7  | SEARCH SILOS
# drive_stat = 8  | PUT BALL IN SILO
# drive_stat = 9  | BALL IN SILO, ROTATE AND TURN BACK

while True:
    us_data = ''
    det_c = -1
    buffer = ''  
    select_result = uselect.select([stdin], [], [], 0)
    while select_result[0]:
        input_character = stdin.read(1)
        if input_character != '#':
            buffer += input_character
        else:
            try:
                data = [int(i) for i in buffer.split('|')]
#                 print(data)
                us_data = us_data + " | data: " + str(data)
            except ValueError:
#                 print("Non-integer detected.")
                us_data = us_data + " | Non-integer detected. "
                continue 
            buffer = ''
        select_result = uselect.select([stdin], [], [], 0)
    
    if uart.any():
#         print("received")
        message_bytes = uart.read()
        message = message_bytes.decode('utf-8') 
        us_data = us_data + " | received: " + str(message)
        li = list(message.split(","))
        if(len(li) == 1): 
            drive_stat = int(li[0])
        else:
            continue
#         print(drive_stat)
        us_data = us_data + " | Drive Stat: " + str(drive_stat)
    
    if(drive_stat == 0): 
        drive(0,0,0,0)
        
    if data and drive_stat == 7:
#         print("Received data: 0: {}, 1: {}, 2: {}, 3: {}, 4: {}".format(data[0], data[1], data[2], data[3], data[4]))
        us_data = us_data + " | Received data: 0: "+str(data[0])+", 1: "+str(data[1])+", 2: "+str(data[2])+", 3: "+str(data[3])+", 4: "+str(data[4])

        if data[4] == -1:
            drive(0, -6000,0, 6000)
        else:
            wm1 = int(map(data[0], -255, 255, -62000, 62000))
            wm2 = int(map(data[1], -255, 255, -62000, 62000))
            wm3 = int(map(data[2], -255, 255, -62000, 62000))
            wm4 = int(map(data[3], -255, 255, -62000, 62000))
            
            adjust = 0
            # | -1 : No Detection | -3 : Near | -4 : Far | -5 : Aligned
             
            front_left_us = measure_distance(front_left_trig, front_left_echo) 
    #         print("Front Left: ", front_left_us)
            us_data = us_data + " | front_left_us: " + str(front_left_us)
            time.sleep_ms(1) 
            
            front_right_us = measure_distance(front_right_trig, front_right_echo)
    #         print("Front Right: ", front_right_us)
            us_data = us_data + " | front_right_us: " + str(front_right_us)
            time.sleep_ms(1)
            
            if data[4] != -1 and (front_left_us < 120 or front_right_us < 120) and abs(front_left_us-front_right_us) >= 3:
                adjust = 1
                if(front_left_us > front_right_us):
    #                 print("Clockwise 1")
                    us_data = us_data + " | Clockwise 1: "
                    drive(slow,-slow,slow,-slow)
                else:
    #                 print("Anti Clockwise 1")
                    us_data = us_data + " | Anti Clockwise 1: "
                    drive(-slow,slow,-slow,slow)
            
            if data[4] == -5 and adjust == 0:
                data[4] = -3
                wm1 == 0
                wm3 == 0
                
            if adjust == 0:
                mul_fac = 1
    #             print("Before Mapping")
    #             print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))
    #             us_data = us_data + " | Before Mapping: W1: {wm1}, W2: {wm2}, W3: {wm3}, W4: {wm4}"
                us_data = us_data + " | Before Mapping: W1: "+str(wm1)+", W2: "+str(wm2)+", W3: "+str(wm3)+", W4: "+str(wm4)
                    
                if data[4] == -3:
                    if wm1 == 0 and wm3 == 0 and front_left_us <= 110 and front_right_us <= 110:
    #                 if wm1 == 0 and wm3 == 0 and front_left_us < 120 and front_right_us < 120:
    #                     print("Centered")
                        us_data = us_data + " | Centered"
                        while front_left_us > 12 and front_left_us > 12:
    #                         print("Moving near Silo")
                            us_data = us_data + " | Moving near Silo"
                            buffer = ''  
                            select_result = uselect.select([stdin], [], [], 0)
                            while select_result[0]:
                                input_character = stdin.read(1)
                                if input_character != '#':
                                    buffer += input_character
                                else:
                                    try:
                                        data = [int(i) for i in buffer.split('|')]
                        #                 print(data)
                                        us_data = us_data + " | data: " + str(data)
                                    except ValueError:
    #                                     print("Non-integer detected.")
                                        us_data = us_data + " | Non-integer detected."
                                        continue 
                                    buffer = ''
                                select_result = uselect.select([stdin], [], [], 0)
                            wm1 = 0
                            wm2 = -8000
                            wm3 = 0
                            wm4 = 8000
                            drive(wm1*1, wm2*1, wm3*1, wm4*1)
                            
                            front_left_us = measure_distance(front_left_trig, front_left_echo) 
    #                         print("Front Left: ", front_left_us)
                            us_data = us_data + " | front_left_us: " + str(front_left_us)
                            time.sleep_ms(1) 
                            
                            front_right_us = measure_distance(front_right_trig, front_right_echo)
    #                         print("Front Right: ", front_right_us)
                            us_data = us_data + " | front_right_us: " + str(front_right_us)
                            time.sleep_ms(1)
                        drive_stat = 8
                        wm2 = 0
                        wm4 = 0
                        wm1 = 0
                        wm3 = 0
                        message = "{}".format(drive_stat)
                #         print(message)
                        us_data = us_data + " | message: "+str(message)
                        message_bytes = message.encode('utf-8')
                        uart.write(message_bytes)
                        drive_stat = 0
    #                     print("JOB DONE")
                        us_data = us_data + " | JOB DONE"
    #                 if wm1 == 0 and wm3 == 0 and front_left_us > 50 and front_left_us > 50:
    #                     wm2 = -3500
    #                     wm4 = 3500
                    
                    elif front_left_us < 35 or front_right_us < 35:
    #                       print("Aligning")
                        us_data = us_data + " | Moving Back for Aligning" 
                        wm1 = 0
                        wm2 =2201
                        wm3 = 0
                        wm4 = -2201
                    elif front_left_us < 110 or front_right_us < 110:
    #                     print("Aligning")
                        us_data = us_data + " | Aligning"
                        if wm1 < 0:
                            wm1 = -2301
                            wm3 = 2301
                        else:
                            wm1 = 2301
                            wm3 = -2301
                        wm2 = 0
                        wm4 = 0
                
                for min_val, max_val, factor in ranges_silo:
                    if all(min_val <= abs(var) <= max_val for var in (wm1, wm2, wm3, wm4)):
                        mul_fac = factor
                        break

                wm1 = int(mul_fac * wm1)
                wm2 = int(mul_fac * wm2)
                wm3 = int(mul_fac * wm3)
                wm4 = int(mul_fac * wm4) 
                
    #             print("After Mapping")
    #             print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))
    #             print("")
                us_data = us_data + " | After Mapping: W1: "+str(wm1)+", W2: "+str(wm2)+", W3: "+str(wm3)+", W4: "+str(wm4)
                 
                drive(wm1*1, wm2*1, wm3*1, wm4*1) 
        data.clear()
    if data and drive_stat == 1:
#         print("Received data: 0: {}, 1: {}, 2: {}, 3: {}, 4: {}".format(data[0], data[1], data[2], data[3], data[4])) 
        us_data = us_data + " | Received data: 0: "+str(data[0])+", 1: "+str(data[1])+", 2: "+str(data[2])+", 3: "+str(data[3])+", 4: "+str(data[4])
        if -11 <= data[0] <= -5 and data[1] >= -45: # -15 -5 
            data[0] = 0
            data[1] = 0
            data[2] = 0
            data[3] = 0
            drive_stat = 2 # ball is in the range
            det_c = data[4] # class of detected object
#             print("Drive stat 2")
            us_data = us_data + " | Drive stat 2"
        elif data[0] < -11 and data[1] >= -70:  # ANTICLOCK
            data[0] = -6 # 17
            data[1] = 6
            data[2] = -6
            data[3] = 6
        elif -5 < data[0] and data[1] >= -70:  # CLOCK
            data[0] = 6
            data[1] = -6
            data[2] = 6
            data[3] = -6
            
        wm1 = int(map(data[0], -255, 255, -62000, 62000))
        wm2 = int(map(data[1], -255, 255, -62000, 62000))
        wm3 = int(map(data[2], -255, 255, -62000, 62000))
        wm4 = int(map(data[3], -255, 255, -62000, 62000))
        
        mul_fac = 1
#         print("Before Mapping")
#         print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4)) 
        us_data = us_data + " | Before Mapping: W1: "+str(wm1)+", W2: "+str(wm2)+", W3: "+str(wm3)+", W4: "+str(wm4)

             
        for min_val, max_val, factor in ranges:
            if all(min_val <= abs(var) <= max_val for var in (wm1, wm2, wm3, wm4)):
                mul_fac = factor
                break

        wm1 = int(mul_fac * wm1)
        wm2 = int(mul_fac * wm2)
        wm3 = int(mul_fac * wm3)
        wm4 = int(mul_fac * wm4)
        
#         print("After Mapping")
#         print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))
#         print("")
        us_data = us_data + " | After Mapping: W1: "+str(wm1)+", W2: "+str(wm2)+", W3: "+str(wm3)+", W4: "+str(wm4)
             
        drive(wm1*1, wm2*1, wm3*1, wm4*1) 
        data.clear()
        
    if(drive_stat == 2): # ball is in the range (drive_stat 2,3,4)
        
        # go back
        
        drive(0,0,0,0)
        time.sleep(0.05)
        drive(0, 8000,0, -8000)
        time.sleep(0.4)
        
        # open the roller
        
        message = "{}".format(drive_stat) 
#         print(message)
        us_data = us_data + " | message: "+str(message)             
        message_bytes = message.encode('utf-8')
        uart.write(message_bytes)
        time.sleep(0.1)
        drive(0,0,0,0)
        time.sleep(0.1)
        
        # go front
        
        drive(0, -12000,0, 12000)
        time.sleep(1)
        drive(0,0,0,0)
        
        # feed the ball
        
        drive_stat = 3
        if det_c == 2:
            drive_stat = 4 # if purple ball then discard
            
        message = "{}".format(drive_stat)
#         print(message)
        us_data = us_data + " | message: "+str(message)
        message_bytes = message.encode('utf-8')
        uart.write(message_bytes)
        
        # go back
        
        drive(0,0,0,0)
        time.sleep(1.5)
        drive(0, 8000,0, -8000)
        time.sleep(0.4)
        
        drive_stat = 0
    
    if(drive_stat == 5):  # go back for easier feed
        drive(0, 15000,0, -15000)
        time.sleep(0.5)
        drive(0,0,0,0) 
        drive_stat = 1
        message = "{}".format(drive_stat)
#         print(message)
        us_data = us_data + " | message: "+str(message)
        message_bytes = message.encode('utf-8')
        uart.write(message_bytes)
        
    if(drive_stat == 9):  # go back for easier feed
        #         print("Go back and Rotate - BALL search")
        us_data = us_data + " | Go back and Rotate - BALL search"
        drive(0, 20000,0, -20000)
        time.sleep(0.25)
        us_data = us_data + " | Anticlockwise for 0.8 seconds 3"
        drive(-medium,medium,-medium,medium)
        time.sleep_ms(800)
        drive_stat = 1
        message = f"{drive_stat}\n"
    
        # Send the message over USB CDC (print to USB)
        print(message, end='')  
        
    if(drive_stat == 6):
#         print("Go back for ZED - SILO view")
        us_data = us_data + " | Go back for ZED - SILO view"
        drive(0, 30000,0, -30000)
        time.sleep(0.2)
        
        drive_stat = 7
        #align to silo
        
        x, y, z = sensor.read()
        deg = sensor.get_degree(x, y, z)
        while not range_min <= deg <= range_max:
            rotate_speed = 5500
            drive(-slow_us,slow_us,-slow_us,slow_us)
            x, y, z = sensor.read()
            deg = sensor.get_degree(x, y, z)
            
        message = f"{drive_stat}\n"
#         drive(0, -6000,0, 6000)
        # Send the message over USB CDC (print to USB)
        print(message, end='')   
        
        
    if us_data == '':
        pass
    else:
        save_to_csv(us_data)    

# ----------------- END -----------------   
















