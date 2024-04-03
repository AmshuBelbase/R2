#make seperate scripts for it 
#pip install pyserial
from machine import Pin, UART
import utime
import serial
import time

uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))
led = machine.Pin(25, machine.Pin.OUT)
#serial port and baud rate
serial_port = 'COM3'  #update with whatever port it is connected to
baud_rate = 115200  

ser = serial.Serial(serial_port, baud_rate, timeout=1)

try:
    while True:
        data_send = "Hello!"
        ser.write(data_send.encode())
        print(f"Sent: {data_send}")
        time.sleep(10)
        
        if uart.any():
        data= uart.readline().decode().split()
        print("Data Received:", data)
        led.toggle()
        
        #if data == 'ON':
            #led.on()
        #elif data == 'OFF':
            #led.off()
        #else:
            #print("error")
        
    utime.sleep_ms(100)  #delay

except KeyboardInterrupt:
    print("\nProgram terminated")

finally:
    ser.close()


