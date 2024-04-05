import serial
import time
import random

serial_port = '/dev/ttyACM0'
baud_rate = 115200
ser = serial.Serial(serial_port, parity=serial.PARITY_EVEN,
                    stopbits=serial.STOPBITS_ONE, baudrate=baud_rate, timeout = 0.1)


class trying:
    def _init_(self):
        while True:
            trying.call_back(ser)

    @staticmethod
    def call_back(ser):
        ser.flush()
        # Open serial port
        # time.sleep(0.5)
        at = time.time()
        print("Start", at)
        # Define floats to send
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


if __name__ == "__main__":
    obj = trying()
