import select
import sys
import time
import machine

        
poll_obj = select.poll()
poll_obj.register(sys.stdin,1)
while True: 
    if poll_obj.poll(0):
        ch = sys.stdin.readline()
        d = [int(num.strip()) for num in ch.split('|')]
        print(d)
        time.sleep(3)
