from machine import Pin, PWM, UART 
import utime
import time

m1_pwm = PWM(Pin(7))
m1_dir = Pin(3, Pin.OUT)
m2_pwm = PWM(Pin(6))
m2_dir = Pin(2, Pin.OUT)
m3_pwm = PWM(Pin(21))
m3_dir = Pin(27, Pin.OUT)
m4_pwm = PWM(Pin(20))
m4_dir = Pin(26, Pin.OUT)

front_left_trig = Pin(17, Pin.OUT)
front_left_echo = Pin(16, Pin.IN)

front_right_trig = Pin(12, Pin.OUT)
front_right_echo = Pin(13, Pin.IN)

left_front_trig = Pin(19, Pin.OUT)
left_front_echo = Pin(18, Pin.IN)

left_back_trig = Pin(22, Pin.OUT)
left_back_echo = Pin(28, Pin.IN)

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

print("Started")
time.sleep(15)
while True:
    front_left_us1 = measure_distance(front_left_trig, front_left_echo) #front_right_trig
    if(front_left_us1 < 10):
        front_left_us2 = measure_distance(front_left_trig, front_left_echo)
        front_left_us = (front_left_us1+front_left_us2)//2
    else:
        front_left_us = front_left_us1 
    
    print("Front Left: ", front_left_us)
    
    front_right_us1 = measure_distance(front_right_trig, front_right_echo)
    if(front_right_us1 < 10):
        front_right_us2 = measure_distance(front_right_trig, front_right_echo)
        front_right_us = (front_right_us1+front_right_us2)//2
    else:
        front_right_us = front_right_us1
        
    
    print("Front Right: ", front_right_us)
    
    left_front_us = measure_distance(left_front_trig, left_front_echo)
    print("Left 1: ", left_front_us)
    
    left_back_us = measure_distance(left_back_trig, left_back_echo)
    print("Left 2: ", left_back_us)
     
    
    if(front_left_us <= 80): # move right when front less than 80
        print(" Move Right >>>>>>>>>>>>")
        drive(-7500,0,7500,0) 
    elif(front_left_us > 80 and (left_front_us < 100 and left_back_us < 100)): # when left less than 100 and front <10 and >80
        if(left_front_us > 80 or left_back_us > 80):
            print("Stop1 ..................")
            drive(0,0,0,0)
        elif(left_front_us < 13 and left_back_us < 13):
            print("Diagonal Front Right ///////////////")
            drive(-7500,-7500,7500,7500)
        elif(left_front_us > 20 and left_back_us > 20):
            print("Diagonal Front Left \\\\\\\\\\\\\\\\\\")
            drive(7500,-7500,-7500,7500)
        elif(left_front_us > left_back_us and (left_front_us - left_back_us) > 6):
            print("Anti - Clockwise <<<<<<<<<<<\\\\\\\\\\\\")
            drive(2500,-2500,2500,-2500)
        elif(left_back_us > left_front_us and (left_back_us - left_front_us) > 6):
            print("Clockwise >>>>>>>>>>>>>>>>>>///////////////")
            drive(-2500,2500,-2500,2500)
        else:
            print("Straight ||||||||||||||")
            drive(0,-9000,0,9000) 
    else:
        print("Stop2 ..................")
        drive(0,0,0,0)
    time.sleep_us(100)

