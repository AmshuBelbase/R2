# R2 Pico - DRIVE
from machine import Pin, PWM, UART 
import sys
from sys import stdin
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


def save_to_csv(data): 
  with open(csv_filename, "a") as f: 
    f.write(data + "\n")

# ----------------- INITIAL POSITIONS -----------------

print("Warming Up")
drive(0,0,0,0)

i = 1
time_s = 5       
led_pin.value(0)
while i<=time_s:
    i=i+1
    led_pin.value(1)
    time.sleep_ms(500)
    led_pin.value(0)
    time.sleep_ms(500)
led_pin.value(1)

print("Started")


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
    
# ----------------- GLOBAL AVRIABLES -----------------

data = []  

drive_stat = 7
right_move = 1

slow = 3800
medium = 8000
fast = 20000
fast_med = 16000
super_fast = 36000
d = 18000

garbage_c = 0
forward_c = 0

csv_filename = "us_data.csv"

# ----------------- MAIN CODE -----------------


message = "{}".format(drive_stat)
print(message)
message_bytes = message.encode('utf-8')
uart.write(message_bytes)
time.sleep_ms(5)
save_to_csv(" ------------------- NEW ATTEMPT -------------------")
while False:
    
    print("loop") 
    us_data = ''
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
            except ValueError:
                print("Non-integer detected.")
                continue 
            buffer = ''
        select_result = uselect.select([stdin], [], [], 0)  

    
    left_back_us = measure_distance(left_back_trig, left_back_echo)  
    print("Left Back: ", left_back_us)
    time.sleep_ms(1)
    us_data = us_data + f" | Left Back: {left_back_us:.2f}"
    
    left_front_us = measure_distance(left_front_trig, left_front_echo)  
    print("Left Front: ", left_front_us)
    time.sleep_ms(1)
    us_data = us_data + f" | Left Front: {left_front_us:.2f}"
    
    front_left_us = measure_distance(front_left_trig, front_left_echo) 
    print("Front Left: ", front_left_us)        
    time.sleep_ms(1)
    us_data = us_data + f" | Front Left: {front_left_us:.2f}"
    
    front_right_us = measure_distance(front_right_trig, front_right_echo)
    print("Front Right: ", front_right_us)
    time.sleep_ms(1)
    us_data = us_data + f" | Front Right: {front_right_us:.2f}"

#     right_front_us = measure_distance(right_front_trig, right_front_echo)  
#     print("Right Front: ", right_front_us)
#     time.sleep_ms(1)
#     us_data = us_data + f" | Right Front: {right_front_us:.2f}"
    
    if(front_left_us <=140 and front_right_us <= 140):
        d = medium
    else:
        d = fast
        
    if(front_left_us <= 45 and front_right_us <= 45):
        if(abs(front_left_us-front_right_us) >= 2):
            if(front_left_us > front_right_us):
                print("Clockwise 1")
                us_data = us_data + " | Clockwise 1"
                drive(slow,-slow,slow,-slow)
            else:
                print("Anti Clockwise 1")
                us_data = us_data + " | Anti Clockwise 1"
                drive(-slow,slow,-slow,slow)
        elif(front_left_us <= 12 and front_right_us <= 12): 
            print("Back 1")
            us_data = us_data + " | Back 1"
            drive(0,slow,0,-slow)
        elif(front_left_us <= 20 and front_right_us <= 20): #and right_front_us > 160
            print("Move Right 1")
            us_data = us_data + " | Move Right 1"
            drive(fast_med,0,-fast_med,0)
        else:
            print("Front 1")
            us_data = us_data + " | Front 1"
            drive(0,-slow,0,slow)
    elif(left_front_us <= 40 and left_back_us <= 40):
        if(abs(left_front_us-left_back_us) >= 4):
            if(left_back_us > left_front_us):
                print("Clockwise 2")
                us_data = us_data + " | Clockwise 2"
                drive(slow,-slow,slow,-slow)
            else:
                print("Anti Clockwise 2")
                us_data = us_data + " | Anti Clockwise 2"
                drive(-slow,slow,-slow,slow)
        elif(left_front_us <= 10 and left_back_us <= 10):
            print("Diagonal Front Right 2")
            us_data = us_data + " | Diagonal Front Right 2"
            drive(slow,-slow,-slow,slow)
        elif(left_front_us <= 27 and left_back_us <= 27):
            print("Straight 2")
            us_data = us_data + " | Straight 2"
            drive(0,-d,0,d)
        else:
            print("Diagonal Front Left 2")
            us_data = us_data + " | Diagonal Front Left 2"
            drive(-slow,-slow,slow,slow) 
    elif(front_right_us > 45 and front_left_us < 45):
        print("Moving right 6")
        us_data = us_data + " | Moving right 6"
        drive(slow,0,-slow,0)
    elif(front_left_us >= 45 and front_right_us >= 45):
        print("Stop 3")
        us_data = us_data + " | Stop 3"
        drive(0,0,0,0)
        forward_c += 1
        print("forward_c:",forward_c)
        us_data = us_data + " | forward_c: " + str(forward_c)
        if(forward_c >= 5):
            print("Moving right for 0.7 seconds 3")
            us_data = us_data + " | Moving right for 0.7 seconds 3"
            drive(medium,0,-medium,0)
            time.sleep(0.7)
            print("Moving straight for 2 seconds 3")
            us_data = us_data + " | Moving straight for 2 seconds 3"
            drive(0,-super_fast,0,super_fast)
            time.sleep(2)
            print("Anticlockwise for 0.8 seconds 3")
            us_data = us_data + " | Anticlockwise for 0.8 seconds 3"
            drive(-medium,medium,-medium,medium)
            time.sleep_ms(800)
            us_data = us_data + " | Moving straight for 2 seconds 3"
            drive(0,-medium,0,medium)
            time.sleep(2)
            print("Stop 3")
            us_data = us_data + " | Stop 3"
            drive(0,0,0,0)
            drive_stat = 1 #1
            break 
    else:
        print("Stop - Confused 7")
        us_data = us_data + " | Stop - Confused 7"
        drive(0,0,0,0)
        garbage_c += 1
        print("garbage_c:",garbage_c)
        us_data = us_data + " | garbage_c: " + str(garbage_c)
        if(garbage_c >= 2):
            pass
    time.sleep_ms(2)
    save_to_csv(us_data)
    
message = "{}".format(drive_stat)
print(message)
message_bytes = message.encode('utf-8')
uart.write(message_bytes)

ranges_silo = [
    (0,250, 20),
    (0,500, 15),
    (0, 1000, 8),
    (0, 2000, 5), 
    (0, 4000, 2),
    (0, 5000, 1.2) 
]
ranges = [
    (0,250, 20),
    (0,500, 15),
    (0, 1000, 8),
    (0, 2000, 5), 
    (0, 4000, 2),
    (0, 5000, 1.2),
    (0, 10000, 0.5),
    (0, 20000, 0.35),
    (0, 62000, 0.3)
]

# ----------------- DRIVE STATUS -----------------

# drive_stat = 0  | STOP 
# drive_stat = 1  | FOLLOW LAPTOP, STOP ROLLER AT 500, GATE CLOSED
# drive_stat = 2  | BALL IN RANGE, GO BACK, OPEN ROLLER AT 180, GO FRONT
# drive_stat = 3  | FEED BALL
# drive_stat = 4  | FEED BALL, DISCARD, drive_stat = 1
# drive_stat = 5  | GO BACK FOR EASIER FEED
# drive_stat = 6  | SEARCH SILOS

while True:
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
            except ValueError:
                print("Non-integer detected.")
                continue 
            buffer = ''
        select_result = uselect.select([stdin], [], [], 0)
    
    if uart.any():
        print("received")
        message_bytes = uart.read()
        message = message_bytes.decode('utf-8')
        li = list(message.split(","))
        if(len(li) == 1): 
            drive_stat = int(li[0])
        else:
            continue
        print(drive_stat)
    
    if(drive_stat == 0): 
        drive(0,0,0,0)
        
    if data and drive_stat == 7:
        print("Received data: 0: {}, 1: {}, 2: {}, 3: {}, 4: {}".format(data[0], data[1], data[2], data[3], data[4]))
        wm1 = int(map(data[0], -255, 255, -62000, 62000))
        wm2 = int(map(data[1], -255, 255, -62000, 62000))
        wm3 = int(map(data[2], -255, 255, -62000, 62000))
        wm4 = int(map(data[3], -255, 255, -62000, 62000))
        
        adjust = 0
        # -2 : Yellow | -1 : No Detection | -3 : Near | -4 : Far | -5 : Aligned
         
        front_left_us = measure_distance(front_left_trig, front_left_echo) 
        print("Front Left: ", front_left_us)        
        time.sleep_ms(1) 
        
        front_right_us = measure_distance(front_right_trig, front_right_echo)
        print("Front Right: ", front_right_us)
        time.sleep_ms(1)
        
        if data[4] == -2 and front_left_us < 10 and front_right_us < 10 and abs(front_left_us-front_right_us) < 2:
            adjust = 1
            drive(0,medium,0,-medium)
            time.sleep(0.5)
            if right_move == 1:
                print("Move Right for a Second")
                drive(medium,0,-medium,0)
                time.sleep(1)
                drive(0,0,0,0)
                right_move = 0
            else:
                print("Move Left for a Second")
                drive(-medium,0,medium,0)
                time.sleep(1)
                drive(0,0,0,0)
                right_move = 1
        
        if data[4] != -1 and front_left_us < 120 and front_right_us < 120 and abs(front_left_us-front_right_us) >= 3:
            adjust = 1
            if(front_left_us > front_right_us):
                print("Clockwise 1")

                drive(slow,-slow,slow,-slow)
            else:
                print("Anti Clockwise 1")

                drive(-slow,slow,-slow,slow)
        
#         if data[4] == -5 and adjust == 0: 
#             if front_left_us < 70 or front_right_us < 70:
#                 adjust = 1
#                 print("stop")
#                 drive(-0,0,-0,0)
            
        if adjust == 0:
            mul_fac = 1
            print("Before Mapping")
            print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))
                
            if data[4] == -3:
#                 if wm1 == 0 and wm3 == 0 and front_left_us <= 50 and front_left_us <= 50:
                if wm1 == 0 and wm3 == 0 and front_left_us < 120 and front_right_us < 120:
                    print("Centered")
                    while front_left_us > 2 and front_left_us > 2:
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
                                except ValueError:
                                    print("Non-integer detected.")
                                    continue 
                                buffer = ''
                            select_result = uselect.select([stdin], [], [], 0)
                        wm1 = 0
                        wm2 = -3500
                        wm3 = 0
                        wm4 = 3500
                        drive(wm1*1, wm2*1, wm3*1, wm4*1)
                        
                        front_left_us = measure_distance(front_left_trig, front_left_echo) 
                        print("Front Left: ", front_left_us)        
                        time.sleep_ms(1) 
                        
                        front_right_us = measure_distance(front_right_trig, front_right_echo)
                        print("Front Right: ", front_right_us)
                        time.sleep_ms(1)
                    drive_stat = 0
                    wm2 = 0
                    wm4 = 0
                    wm1 = 0
                    wm3 = 0
#                 if wm1 == 0 and wm3 == 0 and front_left_us > 50 and front_left_us > 50:
#                     wm2 = -3500
#                     wm4 = 3500
                elif front_left_us < 100 or front_right_us < 100:
                    print("Aligning")
                    if wm1 < 0:
                        wm1 = -2001
                        wm3 = 2001
                    else:
                        wm1 = 2001
                        wm3 = -2001
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
            
            print("After Mapping")
            print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))
            print("")
            drive(wm1*1, wm2*1, wm3*1, wm4*1) 
        data.clear()
    if data and drive_stat == 1:
        print("Received data: 0: {}, 1: {}, 2: {}, 3: {}, 4: {}".format(data[0], data[1], data[2], data[3], data[4]))
        
        if -13 <= data[0] <= -7 and data[1] >= -43: # -15 -5
            data[0] = 0
            data[1] = 0
            data[2] = 0
            data[3] = 0
            drive_stat = 2 # ball is in the range
            det_c = data[4] # class of detected object
            print("Drive stat 2")
        elif data[0] < -13 and data[1] >= -70:  # ANTICLOCK
            data[0] = -8 # 17
            data[1] = 8
            data[2] = -8
            data[3] = 8
        elif -7 < data[0] and data[1] >= -70:  # CLOCK
            data[0] = 8
            data[1] = -8
            data[2] = 8
            data[3] = -8
            
        wm1 = int(map(data[0], -255, 255, -62000, 62000))
        wm2 = int(map(data[1], -255, 255, -62000, 62000))
        wm3 = int(map(data[2], -255, 255, -62000, 62000))
        wm4 = int(map(data[3], -255, 255, -62000, 62000))
        
        mul_fac = 1
        print("Before Mapping")
        print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))

        for min_val, max_val, factor in ranges:
            if all(min_val <= abs(var) <= max_val for var in (wm1, wm2, wm3, wm4)):
                mul_fac = factor
                break

        wm1 = int(mul_fac * wm1)
        wm2 = int(mul_fac * wm2)
        wm3 = int(mul_fac * wm3)
        wm4 = int(mul_fac * wm4)
        
        print("After Mapping")
        print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))
        print("")
        drive(wm1*1, wm2*1, wm3*1, wm4*1) 
        data.clear()
        
    if(drive_stat == 2): # ball is in the range (drive_stat 2,3,4)
        
        # go back
        
        drive(0,0,0,0)
        time.sleep(0.1)
        drive(0, 8000,0, -8000)
        time.sleep(0.4)
        
        # open the roller
        
        message = "{}".format(drive_stat) 
        print(message)
        message_bytes = message.encode('utf-8')
        uart.write(message_bytes)
        time.sleep(0.25)
        drive(0,0,0,0)
        time.sleep(0.1)
        
        # go front
        
        drive(0, -8000,0, 8000)
        time.sleep(1.15)
        drive(0,0,0,0)
        
        # feed the ball
        
        drive_stat = 3
        if det_c == 2:
            drive_stat = 4 # if purple ball then discard
            
        message = "{}".format(drive_stat)
        print(message)
        message_bytes = message.encode('utf-8')
        uart.write(message_bytes)
        
        drive_stat = 0
    
    if(drive_stat == 5):  # go back for easier feed
        drive(0, 5000,0, -5000)
        time.sleep(0.5)
        drive(0,0,0,0) 
        drive_stat = 0
        
    if(drive_stat == 6):
        print("Go back for ZED - SILO view")
        drive(0, 5000,0, -5000)
        time.sleep(2)
        drive_stat = 0
        
        
        

# ----------------- END -----------------   