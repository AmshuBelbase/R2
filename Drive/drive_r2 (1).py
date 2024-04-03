from machine import Pin, PWM, UART
from ibus import IBus
import utime

m1_pwm= PWM(Pin(7))
m1_dir=Pin(3, Pin.OUT)
m2_pwm =PWM(Pin(6))
m2_dir=Pin(2, Pin.OUT)
m3_pwm= PWM(Pin(21))
m3_dir=Pin(27, Pin.OUT)
m4_pwm= PWM(Pin(20))
m4_dir=Pin(26, Pin.OUT)

ibus_in = IBus(1)


# Function to convert the values
def map(val, loval, hival, tolow, tohigh):
    if loval <= val <= hival:
        return (val - loval) / (hival - loval) * (tohigh - tolow) + tolow
    else:
        raise ValueError


def drive(speed1, speed2, speed3, speed4):
    
    m1_pwm.freq(100)
    if speed1<0:
         print("-")
         m1_dir.off()
         m1_pwm.duty_u16(abs(speed1))     #absolute speed
    elif speed1>0:
         print("+")
         
         m1_dir.on()
         m1_pwm.duty_u16(speed1) 
    else:
        m1_pwm.duty_u16(0)
        
    m2_pwm.freq(100)
    if speed2<0:
         print("-")
         m2_dir.value(0)
         m2_pwm.duty_u16(abs(speed2))     #absolute speed
    elif speed2>0:
         print("+")
         m2_dir.value(1)
         m2_pwm.duty_u16(speed2) 
    else:
        m2_pwm.duty_u16(0)
     
        
    m3_pwm.freq(100)
    if speed3<0:
         print("-")
         m3_dir.value(0)
         m3_pwm.duty_u16(abs(speed3))     #absolute speed
    elif speed3>0:
         print("+")
         m3_dir.value(1)
         m3_pwm.duty_u16(speed3) 
    else:
        m3_pwm.duty_u16(0)
        
        
    m4_pwm.freq(100)
    if speed4<0:
         print("-")
         m4_dir.value(0)
         m4_pwm.duty_u16(abs(speed4))     #absolute speed
    elif speed4>0:
         print("+")
         m4_dir.value(1)
         m4_pwm.duty_u16(speed4) 
    else:
        m4_pwm.duty_u16(0)
     
def calc_motor_speed(vx, vy, omega):
    w1 = int(15.75 * vx + (-5.66909078166105) * omega)
    w2 = int(0 + 15.75 * vy + 5.66909078166105 * omega)
    w3 = int((-15.75) * vx + 0 + 5.66909078166105 * omega)
    w4 = int(0 + (-15.75) * vy + (-5.66909078166105) * omega)
    
    return w1, w2, w3, w4


    

while True:
    res = ibus_in.read()
    # if signal then display immediately
    if res[0] == 1:
#         print("Status {} CH 1 {} Ch 2 {} Ch 3 {} Ch 4 {} Ch 5 {} Ch 6 {} - {}".format(
#             res[0],
#             IBus.normalize(res[1]),
#             IBus.normalize(res[2]),
#             IBus.normalize(res[3]),
#             IBus.normalize(res[4]),
#             IBus.normalize(res[5]),
#             IBus.normalize(res[6]),
#             utime.ticks_ms()
#         ))
               
        
    vx = IBus.normalize(res[2])
    if(vx<=-6 and vx>=-100):
        vx = map(vx, -100, -6, -100, 0)
    elif(vx>-6 and vx<=93):
        vx = map(vx, -6, 93, 0, 100)
        
    vy = IBus.normalize(res[1])
    if(vy<=-6 and vy>=-100):
        vy = map(vy, -99, -15, -100, 0)
    elif(vy>-6 and vy<=93):
        vy = map(vy, -15, 84, 0, 100)
        
    omega = IBus.normalize(res[4])
    if(omega<=-1 and omega>=-100):
        omega = map(omega, -100, -1, -100, 0)
    elif(omega>-1 and omega<=98):
        omega = map(omega, -1, 98, 0, 100)
        
    if vx ==0 and vy==0 and omega==0:
        drive(0,0,0,0)
        
    w1, w2, w3, w4 = calc_motor_speed(vx, vy, omega)
    
    # Set motor speeds
    wm1=int(map(w1, -1575, 1575, -19660, 19660))
    wm2=int(map(w2, -1575, 1575, -19660, 19660))
    wm3=int(map(w3, -1575, 1575, -19660, 19660))
    wm4=int(map(w4, -1575, 1575, -19660, 19660))
    
    if omega<-10 and omega>10:
        drive(-2*w1,2*w2,2*w3,2*w4)
    utime.sleep_ms(10)