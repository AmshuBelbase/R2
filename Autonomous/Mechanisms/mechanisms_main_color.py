from machine import Pin, UART, PWM
from servo import Servo 
from Stepper import StepperMotor 
import time
import utime
import sys
from time import sleep
from machine import Pin, SoftI2C

from tcs34725 import *  # class library of color

# ----------------- PINOUTS -----------------

time.sleep(1)

uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))  

# roller servo
roller_servo_r_pin =3 # 3
roller_servo_l_pin = 10
roller_servo1 = Servo(roller_servo_r_pin)
roller_servo2 = Servo(roller_servo_l_pin)

# gate servo
gate_servo_r_pin = 7 # 7
gate_servo_l_pin = 6 # 6
gate_servo1 = Servo(gate_servo_r_pin)
gate_servo2 = Servo(gate_servo_l_pin)

# push servo
push_servo_r_pin = 2 # 2
push_servo_l_pin = 11 # 11
push_servo1 = Servo(push_servo_r_pin)
push_servo2 = Servo(push_servo_l_pin)
 

# roller dc motor
roller_pin1 = Pin(15, Pin.OUT)
roller_pin2 = Pin(14, Pin.OUT)

# elevator steppers
elevator_step1_pin = 16
elevator_dir1_pin = 17
stepper_motor = StepperMotor(elevator_step1_pin, elevator_dir1_pin)

#ultrasonics

roller_trig = Pin(22, Pin.OUT)
roller_echo = Pin(26, Pin.IN)

elevator_trig = Pin(27, Pin.OUT)
elevator_echo = Pin(28, Pin.IN)

# left_trig = Pin(20, Pin.OUT)   
# left_echo = Pin(21, Pin.IN)
# 
# right_trig = Pin(18, Pin.OUT) 
# right_echo = Pin(19, Pin.IN)


# ----------------- INITIAL POSITIONS -----------------

drive_stat = 30
message = "{}".format(drive_stat)
print("Sent: ",message)
message_bytes = message.encode('utf-8')
uart.write(message_bytes)

gate_servo1.goto(120) 
gate_servo2.goto(880)
 

push_servo1.goto(700) 
push_servo2.goto(300)

roller_pin1.value(1)
roller_pin2.value(0)
 
x_deg = roller_servo1.get_position() 
roller = 0
while x_deg != roller:
    if(x_deg > roller):
        x_deg = x_deg -1
    else:
        x_deg = x_deg +1 
    y_deg = 1024 - x_deg
    roller_servo1.goto(x_deg) 
    roller_servo2.goto(y_deg)
    time.sleep_us(1000)
    
# stepper_motor.stepper_up(2150)
time.sleep(0.1)
# stepper_motor.stepper_down(2150)
push_servo1.goto(0) 
push_servo2.goto(1000) 

roller_pin1.value(1)
roller_pin2.value(0)

time.sleep_ms(300)

roller_pin1.value(0)
roller_pin2.value(0)    


# ----------------- GLOBAL AVRIABLES -----------------

drive_stat = 0

# ----------------- USER DEFINED FUNCTIONS -----------------

def detect_color(counts_history):
    """ Determine the color based on the largest value being consistent for 3 consecutive readings """
    #p_max = all((counts[1] > counts[2] and counts[1] > counts[3]) and counts[2] > counts[3] for counts in counts_history)
    p_max = False
    b_max = False
    r_max = False
    g_max = False
    for counts in counts_history:
        if (counts[1] > counts[2] and counts[1] > counts[3] and counts[3] > counts[2]):
            #if(counts[3] > counts[2]):
                p_max=True
        elif (counts[1] > counts[2] and counts[1] > counts[3]):
            r_max=True
        elif (counts[2] > counts[1] and counts[2] > counts[3]):
            g_max=True
        elif (counts[3] > counts[2] and counts[3] > counts[1]):
            b_max=True
        
    '''   
    r_max = all(counts[1] > counts[2] and counts[1] > counts[3] for counts in counts_history)
    g_max = all(counts[2] > counts[1] and counts[2] > counts[3] for counts in counts_history)
    b_max = all(counts[3] > counts[1] and counts[3] > counts[2] for counts in counts_history)
    '''
    
                
            
    
    if p_max:
        return "Purple"
    elif r_max:
        return "Red"
    elif g_max:
        return "-"
    elif b_max:
        return "Blue"
    else:
        return "-"

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

    # Distance = (duration * speed of sound) / 2
    distance = duration * 34300 / (2 * 1000000)  # Convert microseconds to seconds

    return distance




# ----------------- MAIN CODE -----------------

led_pin = Pin(25, Pin.OUT)
led_pin.value(1)

print("Starting tcs34725_test program")
if sys.platform == "pyboard":  # test with PyBoard
    tcs = TCS34725(scl=Pin("B6"), sda=Pin("B7"))  # instance of TCS34725 on pyboard
else:  # test with ESP32 board
    tcs = TCS34725(scl=Pin(9), sda=Pin(8))  # instance of TCS34725 on ESP32
if not tcs.isconnected:  # terminate if not connected
    print("Terminating...")
    sys.exit()
tcs.gain = TCSGAIN_LOW
tcs.integ = TCSINTEG_HIGH
tcs.autogain = False  # use autogain!

counts_history = []  

while True:
    if uart.any(): 
        message_bytes = uart.read()
        message = message_bytes.decode('utf-8')
        li = list(message.split(","))
        if(len(li) == 1): 
            drive_stat = int(li[0])
        else:
            continue
        print("Received: ",drive_stat)
    if(drive_stat == 1):
        roller_pin1.value(0)
        roller_pin2.value(0)
        gate_servo1.goto(120) 
        gate_servo2.goto(880)
        x_deg = roller_servo1.get_position() 
        roller = 350
        while x_deg != roller:
            if(x_deg > roller):
                x_deg = x_deg -1
            else:
                x_deg = x_deg +1 
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)
            time.sleep_us(1000)
    if(drive_stat == 2): 
        roller_pin1.value(1)
        roller_pin2.value(0)
        x_deg = roller_servo1.get_position() 
        roller = 0
        while x_deg != roller:
            if(x_deg > roller):
                x_deg = x_deg -1
            else:
                x_deg = x_deg +1 
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)
            time.sleep_us(1000)
    if drive_stat == 8:
        push_servo1.goto(1000) 
        push_servo2.goto(0)
        stepper_motor.stepper_up(1000)
        push_servo1.goto(0) 
        push_servo2.goto(1000)
        time.sleep(2)
        drive_stat = 9
        message = "{}".format(drive_stat)
        print("Sent: ",message)
        message_bytes = message.encode('utf-8')
        uart.write(message_bytes)
        stepper_motor.stepper_down(2150)
        push_servo1.goto(700) 
        push_servo2.goto(300)
        drive_stat = 1
    if(drive_stat == 3 or drive_stat == 4):
        
        if drive_stat == 3: # if red or blue ball then feed
            gate_servo1.goto(120) 
            gate_servo2.goto(880)
        elif drive_stat == 4: # if purple ball then discard
            gate_servo1.goto(700) 
            gate_servo2.goto(300)   
                  
        roller_pin1.value(1)
        roller_pin2.value(0)
        
        print("At 150")
        x_deg = 150    # 150
        y_deg = 1024 - x_deg
        roller_servo1.goto(x_deg) 
        roller_servo2.goto(y_deg)

        time.sleep(1.5)  

        print("At 350")
        x_deg = 350    # 150
        y_deg = 1024 - x_deg
        roller_servo1.goto(x_deg) 
        roller_servo2.goto(y_deg)
        
#         roller_pin1.value(0)
#         roller_pin2.value(1)
#         time.sleep(2)
#         roller_pin1.value(1)
#         roller_pin2.value(0)

        c = 0
        start_time = utime.ticks_ms()
        while utime.ticks_diff(utime.ticks_ms(), start_time) < 3000:  # 3000 ms = 3 seconds
            roller_us = measure_distance(roller_trig, roller_echo)
            print("roller_us: ", roller_us)
            
            if roller_us < 10:
                start_time = utime.ticks_ms()
                c += 1
            else:
                c = 0
            
            time.sleep_ms(10)

            # Check if c has been incremented 60 times (meaning elevator < 4 for 60 consecutive iterations)
            if c > 40:
                break

        # If loop terminated due to timeout
        if utime.ticks_diff(utime.ticks_ms(), start_time) >= 3000:
            print("Loop terminated due to timeout.") 
            roller_pin1.value(0)
            roller_pin2.value(1) 

#             time.sleep(0.5)
            
            drive_stat = 4  
        else:
            
            if drive_stat == 3:
        
                count_color = 0
                count_color_seq = 0 
                
                print(" Clear   Red Green  Blue    gain  >")
                try:
                    while count_color <=20:
                        count_color +=1
                        """ show color counts """
                        counts_tuple = tcs.colors  # obtain all counts
                        counts = list(counts_tuple)  # list of 4 counts
                        for count in counts_tuple:
                            # show 'absolute' light value (count / gain-factor)
                            if count >= tcs.overflow_count:  # overflow?
                                count = -1  # overflow reported as count -1
                            print(" {:5d}".format(count // tcs.gain_factor), end="")
                        
                        counts_history.append(counts)
                        if len(counts_history) > 3:
                            counts_history.pop(0)  # keep only the last 3 readings

                        if len(counts_history) == 3:
                            color = detect_color(counts_history)
                        else:
                            color = "-"

                        red = counts[1]
                        green = counts[2]
                        blue = counts[3]
                        
                        if color == "Blue" or color == "Red":
                            count_color_seq +=1
                        else:
                            count_color_seq = 0

                        """if color == "-" and is_purple(red, green, blue):
                            color = "Purple"
                             """

                        print("    ({:2d})  {:s}" .format(tcs.gain_factor, color))
                        sleep(0.1)  # interval between reads

                except KeyboardInterrupt:
                    print("Closing down!")

                except Exception as err:
                    print("Exception:", err)
                    
                    
                if count_color_seq <= 13:
                    gate_servo1.goto(700) 
                    gate_servo2.goto(300)
                    drive_stat = 4
            
            print("At 500")
            x_deg = 500    # 150
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)

            time.sleep(0.5)


            print("At 1000")
            x_deg = 1024    # 150
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)

        
        if drive_stat == 4: # if purple ball then again start searching
            time.sleep(0.5)
            print("At 0")
            x_deg = 0    # 150
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)
            roller_pin1.value(0)
            roller_pin2.value(1)
            drive_stat = 5
            message = "{}".format(drive_stat)
            print("Sent: ",message)
            message_bytes = message.encode('utf-8')
            uart.write(message_bytes)
            drive_stat = 1
            print("At 0")
            x_deg = 350    # 150
            y_deg = 1024 - x_deg
            roller_servo1.goto(x_deg) 
            roller_servo2.goto(y_deg)
            time.sleep(1.5)
            
        else:
            print("At elevator")
            c = 0
            start_time = utime.ticks_ms()
            while utime.ticks_diff(utime.ticks_ms(), start_time) < 4500:  # 3000 ms = 3 seconds
                elevator = measure_distance(elevator_trig, elevator_echo)
                print("elevator: ", elevator)
                
                if elevator <= 13:
                    start_time = utime.ticks_ms()
                    c += 1
                else:
                    c = 0
                
                time.sleep_ms(5)

                # Check if c has been incremented 60 times (meaning elevator < 4 for 60 consecutive iterations)
                if c > 60:
                    break

            # If loop terminated due to timeout
            if utime.ticks_diff(utime.ticks_ms(), start_time) >= 4500:
                print("Loop terminated due to timeout.")
                drive_stat = 5
                message = "{}".format(drive_stat)
                print("Sent: ",message)
                message_bytes = message.encode('utf-8')
                uart.write(message_bytes)
                drive_stat = 5
            else:
                gate_servo1.goto(700) 
                gate_servo2.goto(300)
                push_servo1.goto(700) 
                push_servo2.goto(300)
                
                drive_stat = 6
                message = "{}".format(drive_stat)
                print("Sent: ",message)
                message_bytes = message.encode('utf-8')
                uart.write(message_bytes)
                
                print("At 500")
                x_deg = 500    # 150
                y_deg = 1024 - x_deg
                roller_servo1.goto(x_deg) 
                roller_servo2.goto(y_deg)
                
                stepper_motor.stepper_up(1150)
        roller_pin1.value(0)
        roller_pin2.value(0)



