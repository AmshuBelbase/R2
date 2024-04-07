from machine import Pin, PWM
from ibus import IBus
import utime

ibus_in = IBus(1)
jugad_uart = PWM(Pin(14))
jugad_uart.freq(500)      # Set the frequency value
jugad_uart_value = 0
if __name__ == '__main__':
    while True:
        res = ibus_in.read()
        # if no signal then display immediately
        if res[0] == 0:
            drive(0, 0, 0, 0)
            print("Flysky Not Connected")
            continue 


        step_up_down = IBus.normalize(res[3])
        feed_mech = IBus.normalize(res[5])
        push_mech = IBus.normalize(res[6])
        
        if(feed_mech < -50):
            print("feed_mech")
            jugad_uart_value = 25
        elif(step_up_down > 50 or step_up_down < -50):
            print("step_up_down")
            jugad_uart_value = 50
        elif(push_mech > 50):
            print("push_mech")
            jugad_uart_value = 75
        else:
            jugad_uart_value = 0
            
        print(int(jugad_uart_value * 500))
        jugad_uart.duty_u16(int(jugad_uart_value * 500))     # Set the duty cycle, between 0-65535
        utime.sleep_ms(10)
         