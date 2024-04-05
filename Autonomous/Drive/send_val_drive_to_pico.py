import serial
import time
import random

s = serial.Serial(port="/dev/ttyACM0", parity=serial.PARITY_EVEN,
                  stopbits=serial.STOPBITS_ONE, timeout=1)


class trying:
    def __init__(self):
        while True:
            trying.call_back(s)

    @staticmethod
    def call_back(ser):
        ser.flush()
        at = time.time()
        print("Start", at)

        float1 = random.randint(0, 255)
        float2 = random.randint(0, 255)
        float3 = random.randint(0, 255)
        float4 = random.randint(0, 255)

        # Convert to bytes
        data = (str(float1) + '|' +
                str(float2) + '|' +
                str(float3) + '|' +
                str(float4)) + "\n"

        # Send data
        ser.write(data.encode())
        print(f"Sent: {data}")
        print("End", time.time())
        print("Time taken", time.time() - at)
        time.sleep(0.005)


if __name__ == '__main__':
    obj = trying()
