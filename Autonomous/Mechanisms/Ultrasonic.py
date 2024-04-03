from machine import Pin
import time

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)

    def measure_distance(self):
        # Send a 10us pulse to trigger the sensor
        self.trigger.off()
        time.sleep_us(2)
        self.trigger.on()
        time.sleep_us(10)
        self.trigger.off()

        # Wait for the echo to start
        while self.echo.value() == 0:
            pass
        start_time = time.ticks_us()

        # Wait for the echo to end
        while self.echo.value() == 1:
            pass
        end_time = time.ticks_us()

        # Calculate the duration of the echo pulse
        duration = time.ticks_diff(end_time, start_time)

        # Convert the duration to distance (in cm)
        # Speed of sound = 343 m/s = 34300 cm/s
        # Distance = (duration * speed of sound) / 2
        distance = duration * 34300 / (2 * 1000000)  # Convert microseconds to seconds

        return distance

