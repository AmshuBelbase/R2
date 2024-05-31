from machine import Pin, PWM, UART 
import sys
import time
uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))
count = 0
while True:
    if uart.any():
        message_bytes = uart.read()
        message = message_bytes.decode('utf-8')
        li = list(message.split(","))
        print("Message ", message)
        print("List ", li)
        print("Length : ", len(li))
        count = count + len(li) - 1
        if(len(li) > 1): 
            drive_stat = int(li[len(li)-1])
            if drive_stat%10==0:
                drive_stat = 1
                message = "{}".format(drive_stat)
                print(message)
                message_bytes = message.encode('utf-8')
                uart.write(message_bytes)
        else:
            continue
    else:
        print(".")
    print(count)
    time.sleep(0.8)
