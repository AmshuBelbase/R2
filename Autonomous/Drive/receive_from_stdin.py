import time
import sys
import _thread 
from sys import stdin
import uselect

data = []

while True: 
    buffer = ''  
    select_result = uselect.select([stdin], [], [], 0)
    while select_result[0]:
        input_character = stdin.read(1)
        if input_character != '#':
            buffer += input_character
        else:
            try:
                data = [int(i) for i in buffer.split('|')]
#                 print(data)
            except ValueError:
                print("Non-integer detected.")
                continue 
            buffer = ''
        select_result = uselect.select([stdin], [], [], 0)
    
    if data:
        print("Received data: 0: {}, 1: {}, 2: {}, 3: {}, 4: {}".format(data[0], data[1], data[2], data[3], data[4]))

        if -13 <= data[0] <= -7 and data[1] >= -43: # -15 -5
            data[0] = 0
            data[1] = 0
            data[2] = 0
            data[3] = 0
            print("Drive stat 2")
        elif data[0] < -13 and data[1] >= -70:  # ANTICLOCK
            print("ANTICLOCK")
            data[0] = -17
            data[1] = 17
            data[2] = -17
            data[3] = 17
        elif -7 < data[0] and data[1] >= -70:  # CLOCK
            print("CLOCK")
            data[0] = 17
            data[1] = -17
            data[2] = 17
            data[3] = -17
        
        print("MODIFIED data: 0: {}, 1: {}, 2: {}, 3: {}, 4: {}".format(data[0], data[1], data[2], data[3], data[4]))
        print("")
    time.sleep(0.2)