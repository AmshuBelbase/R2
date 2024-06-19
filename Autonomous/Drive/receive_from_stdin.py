import time
import sys
import _thread 
from sys import stdin
import uselect

data = []
data_lock = _thread.allocate_lock()  # Lock for data access

def Core0():
    global data, data_lock
    buffer = ''
    while True:
        with data_lock:     
          select_result = uselect.select([stdin], [], [], 0)
          buffer = ''
          while select_result[0]:
            input_character = stdin.read(1)
            if input_character != '#':
                buffer += input_character
            else:                    
                try:
                    data = [int(i) for i in buffer.split('|')]
                    print(data)
                except ValueError:
                    print("Non-integer detected.")
                    continue 
                buffer = ''
            select_result = uselect.select([stdin], [], [], 0)        
        time.sleep_ms(1)  # Adjust sleep time as needed

def Core1():
    global data, data_lock
    while True: 
        with data_lock: 
            if data:
                print("Received data: 1: {}, 2: {}, 3: {}, 4: {}".format(data[0], data[1], data[2], data[3]))
                # Process data here
                data.clear() 
            time.sleep_ms(1)  # Adjust sleep time as needed

_thread.start_new_thread(Core0, ())
Core1()

