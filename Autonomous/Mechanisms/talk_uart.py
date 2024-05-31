from machine import Pin, UART, PWM  
import time
import utime

drive_stat = 1
uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))
count = 0
while True:
    if uart.any():
        message_bytes = uart.read()
        message = message_bytes.decode('utf-8')
        li = list(message.split(","))
        print("Message ", message)
        drive_stat = int(message)
    message = ",{}".format(drive_stat)
    print(message)
    message_bytes = message.encode('utf-8')
    uart.write(message_bytes)
    count = count + 1
    print(count)
    drive_stat = drive_stat + 1
    time.sleep_ms(2)
