from machine import *
from time import sleep,sleep_ms,ticks_ms

# Constants for the encoder pins
PIN_A = 16
PIN_B = 17

# Initialize variables to keep track of encoder state and count
count = 0
last_A = 0
last_B = 0
state = 0
rpm =0# To keep track of encoder state for determining direction
lastTime=0
ppr=650

m1_pwm=PWM(Pin(20))
m1_in1=Pin(26,Pin.OUT,value=0)

current_A=0
current_B=0
def rpm_(c):
    global rpm
    rpm=int((c/ppr)*600)

def drive(speed,in_1,pwm_pin):
        pwm=pwm_pin
        pwm.freq(1000)
        if speed<0:
            in_1.off()
#             in_2.on()
            pwm.duty_u16(abs(speed))
#             print("drive1")
            
        elif speed>0:
             print("drive1el")
             in_1.on()
#              in_2.off()
             pwm.duty_u16(speed)
        else:
             pwm.duty_u16(0)
# #             in_2.on()
# Callback function for the A signal interrupt
def on_encoder_A_irq(pin):
    global count, last_A
    current_A = pin.value()
    current_B = Pin(PIN_B).value()

    if current_A != last_A:
        if current_A == current_B:
            count-=1
        else:
            count+=1
         
    last_A = current_A
    

# Initialize the GPIO pins for the encoder signals
pin_A = Pin(PIN_A, Pin.IN)
pin_B = Pin(PIN_B, Pin.IN)

# Attach interrupt handler to pin A
pin_A.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=on_encoder_A_irq)
# drive(0,m1_in1,m1_pwm)
count_flag = 0
flag=0 
while True and count_flag < 50:
 if(ticks_ms()-lastTime>=100):
    if flag==0:
        drive(0,m1_in1,m1_pwm)
        sleep(5)
        flag=1
    drive(50*257,m1_in1,m1_pwm)
    print("Count: ",count)
    rpm_(count)
    print("RPM: ",rpm ) 
    count=0
    rpm=0
    lastTime=ticks_ms()
    count_flag += 1
drive(0,m1_in1,m1_pwm)  
sleep(1)
