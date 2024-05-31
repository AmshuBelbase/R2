from machine import Pin, PWM, UART 
import utime
import time

m1_pwm = PWM(Pin(21))
m1_dir = Pin(26, Pin.OUT)
m2_pwm = PWM(Pin(20))
m2_dir = Pin(22, Pin.OUT)

m3_pwm = PWM(Pin(17))
m3_dir = Pin(19, Pin.OUT)
m4_pwm = PWM(Pin(16))
m4_dir = Pin(18, Pin.OUT)

left_back_trig = Pin(3, Pin.OUT)
left_back_echo = Pin(4, Pin.IN)

left_front_trig = Pin(7, Pin.OUT)
left_front_echo = Pin(6, Pin.IN)

front_left_trig = Pin(9, Pin.OUT)
front_left_echo = Pin(8, Pin.IN)

front_right_trig = Pin(15, Pin.OUT)
front_right_echo = Pin(14, Pin.IN)

right_front_trig = Pin(13, Pin.OUT)
right_front_echo = Pin(12, Pin.IN)



# m1_pwm = PWM(Pin(7))
# m1_dir = Pin(3, Pin.OUT)
# m2_pwm = PWM(Pin(6))
# m2_dir = Pin(2, Pin.OUT)
# m3_pwm = PWM(Pin(21))
# m3_dir = Pin(27, Pin.OUT)
# m4_pwm = PWM(Pin(20))
# m4_dir = Pin(26, Pin.OUT)



# front_left_trig = Pin(19, Pin.OUT)
# front_left_echo = Pin(18, Pin.IN)
# 
# front_right_trig = Pin(11, Pin.OUT)
# front_right_echo = Pin(10, Pin.IN)
# 
# left_front_trig = Pin(13, Pin.OUT)
# left_front_echo = Pin(12, Pin.IN)
# 
# left_back_trig = Pin(22, Pin.OUT)
# left_back_echo = Pin(28, Pin.IN)
# 
# right_front_trig = Pin(17, Pin.OUT)
# right_front_echo = Pin(16, Pin.IN)

led_pin = Pin(25, Pin.OUT)
led_pin.value(0)

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
# while True:
drive(0,0,0,0)
d = 18000
i = 1
led_pin.value(0)
while i<=3:
    i=i+1
    led_pin.value(1)
    time.sleep_ms(500)
    led_pin.value(0)
    time.sleep_ms(500)
led_pin.value(1)


while True:
    print("loop")
    led_pin.value(1)
    time.sleep_ms(500)
    led_pin.value(0)
    time.sleep_ms(500)
    
    front_right_us = measure_distance(front_right_trig, front_right_echo)
    print("Front Right: ", front_right_us)
    
    left_front_us = measure_distance(left_front_trig, left_front_echo)  
    print("Left Front: ", left_front_us)

    left_back_us = measure_distance(left_back_trig, left_back_echo)  
    print("Left Back: ", left_back_us)
    
    right_front_us = measure_distance(right_front_trig, right_front_echo)  
    print("Right Front: ", right_front_us)
    
    front_left_us = measure_distance(front_left_trig, front_left_echo) 
    print("Front Left: ", front_left_us)
     


while True:
    print("loop")
    front_right_us = measure_distance(front_right_trig, front_right_echo)
    print("Front Right: ", front_right_us)

    front_left_us = measure_distance(front_left_trig, front_left_echo) 
    print("Front Left: ", front_left_us)

    left_front_us = measure_distance(left_front_trig, left_front_echo)  
    print("Left Front: ", left_front_us)

    left_back_us = measure_distance(left_back_trig, left_back_echo)  
    print("Left Back: ", left_back_us)

    right_front_us = measure_distance(right_front_trig, right_front_echo)  
    print("Right Front: ", right_front_us)
    
    if(front_left_us <=140 and front_right_us <= 140):
        d = 9000 # 7000
    else:
        d = 18000 # 18000
    if(right_front_us <128 and front_left_us <= 45 and front_right_us <= 45):
        print("Move Left 4")
        drive(5500,0,-5500,0) # 4000
    elif(front_left_us <= 45 and front_right_us <= 45):
        if(abs(front_left_us-front_right_us) >= 3):
            if(front_left_us > front_right_us):
                print("Clockwise 1")
                drive(-3500,3500,-3500,3500) # 2500
            else:
                print("Anti Clockwise 1")
                drive(3500,-3500,3500,-3500) # 2500
        elif(front_left_us <= 10 and front_right_us <= 10):
            print("Digonal Back Right 1")
            drive(4500,4500,4500,-4500) # 3000
        elif(front_left_us <= 20 and front_right_us <= 20 and right_front_us > 160):
            print("Move Right 1")
            drive(-18000,0,18000,0) #18000
        else:
            print("Diagonal Front Right 1")
            drive(-4500,-4500,4500,4500) # 3000
    elif(left_front_us <= 45 and left_back_us <= 45):
        if(abs(left_front_us-left_back_us) >= 4):
            if(left_back_us > left_front_us):
                print("Clockwise 2")
                drive(-3500,3500,-3500,3500) # 2500
            else:
                print("Anti Clockwise 2")
                drive(3500,-3500,3500,-3500)  # 2500
        elif(left_front_us <= 10 and left_back_us <= 10):
            print("Diagonal Front Right 2")
            drive(-6000,-6000,6000,6000) # 5000
        elif(left_front_us <= 27 and left_back_us <= 27):
            print("Straight 2")
            drive(0,-d,0,d)
        else:
            print("Diagonal Front Left 2")
            drive(6000,-6000,-6000,6000) #5000
    elif(right_front_us >=118 and right_front_us <=128):
        print("Moving straight for 2.5 seconds 3")
        drive(0,-36000,0,36000) # 30000
        time.sleep_ms(1750)
        print("Anticlockwise for 1 seconds 3")
        drive(12000,-12000,12000,-12000) #10000
        time.sleep_ms(500)
        print("Stop 3")
        drive(0,0,0,0)
        break
    elif(right_front_us <128):
        print("Move Left 4")
        drive(5500,0,-5500,0) # 4000
    elif(right_front_us <= 160):
        print("Moving right 5")
        drive(-5500,0,5500,0) # 4000
    elif(front_right_us > 45 and front_left_us < 45):
        print("Moving right 6")
        drive(-5500,0,5500,0) # 4000
    else:
        print("Stop - Confused 7")
        drive(0,0,0,0)
        break
    time.sleep_ms(100)







