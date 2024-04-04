import select
import sys
import time
import machine

# Create an instance of a polling object
poll_obj = select.poll()
# Register sys.stdin (standard input) for monitoring read events with priority 1
poll_obj.register(sys.stdin, 1)
count = 0
while True:
    # Check if there is any data available on sys.stdin without blocking
    if poll_obj.poll(0):
        # Read the line from sys.stdin
        ch = sys.stdin.readline()
        print(ch)
        count += 1
        print(count)
