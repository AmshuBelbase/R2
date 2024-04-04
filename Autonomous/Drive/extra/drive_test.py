from machine import Pin, PWM, UART
import utime

m1_pwm= PWM(Pin(20))
m1_dir=Pin(26)

while(True):
    m1_pwm.freq(100)
    m1_dir.value(1)
    m1_pwm.duty_u16(0)
    utime.sleep_ms(10)
