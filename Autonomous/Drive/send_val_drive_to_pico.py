import serial
import time
import random

s = serial.Serial(port="/dev/ttyACM0", parity=serial.PARITY_EVEN,
                  stopbits=serial.STOPBITS_ONE, timeout=1)



class trying:
    def __init__(self):
        i = 0
        while True:
            trying.call_back(s, i)
            i+=1

    @staticmethod
    def call_back(ser, i):
        ser.flush()
        at = time.time()
        print("Start", at)
        float1 = random.randint(-255, 255)
        float2 = random.randint(-255, 255)
        float3 = random.randint(-255, 255)
        float4 = random.randint(-255, 255)
        
        # Convert to bytes
        data = (str(i) + '|' + str(float1) + '|' +
                str(float2) + '|' +
                str(float3) + '|' +
                str(float4)) + "\n"


        print(f"Sent: {data}")
        # Send data
        ser.write(data.encode()) 
        time.sleep(0.005)


if __name__ == '__main__':
    obj = trying()
