import machine
import utime

# Define the pin connected to the PWM signal
pwm_input_pin = machine.Pin(11, machine.Pin.IN)

# Define a function to measure PWM duty cycle
def measure_pwm_duty_cycle(pin, duration=0.1):
    start_time = utime.ticks_us()
    while not pin.value():
        if utime.ticks_diff(utime.ticks_us(), start_time) > duration * 1000000:
            return None  # Timeout
    pulse_start = utime.ticks_us()
    while pin.value():
        if utime.ticks_diff(utime.ticks_us(), start_time) > duration * 1000000:
            return None  # Timeout
    pulse_end = utime.ticks_us()
    pulse_duration = utime.ticks_diff(pulse_end, pulse_start)
    period_duration = utime.ticks_diff(pulse_end, start_time)
    duty_cycle = (pulse_duration / period_duration) * 100
    return duty_cycle

# Main loop
while True:
    pwm_duty_cycle = measure_pwm_duty_cycle(pwm_input_pin)
    if pwm_duty_cycle is not None:
        print("Received PWM Duty Cycle: {:.2f}%".format(pwm_duty_cycle))
    else:
        pwm_duty_cycle = 0
        print("Timeout occurred while measuring PWM signal {:.2f}%".format(pwm_duty_cycle))
    utime.sleep(0.01)  # Adjust as needed
