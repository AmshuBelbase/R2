import time

from sys import stdin

import uselect

csv_filename = "data.csv"

def save_to_csv(data):

  with open(csv_filename, "a") as f:

    f.write(data + "\n")
    
save_to_csv(" --------------- New Attempt --------------- ")

while True:

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
        
        save_to_csv(buffer)

        buffer = ''

    select_result = uselect.select([stdin], [], [], 0)