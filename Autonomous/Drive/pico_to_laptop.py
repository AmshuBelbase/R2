import sys
import time
 
c = 0
while True:
    c += 1
    # Construct the message you want to send
    message = f"{c}\n"
    
    # Send the message over USB CDC (print to USB)
    print(message, end='') 
    time.sleep(1)