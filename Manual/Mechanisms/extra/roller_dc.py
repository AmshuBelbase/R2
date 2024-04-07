from machine import Pin, PWM
import utime

class BLDCMotor:
    def __init__(self, pwm_pin, dir_pin1, dir_pin2):
        self.pwm = PWM(Pin(pwm_pin))
        self.pwm.freq(9000)
        self.dir1 = Pin(dir_pin1, Pin.OUT)
        self.dir2 = Pin(dir_pin2, Pin.OUT)
        self.dir1.low()
        self.dir2.low()
        self.speed = 0

    def set_speed(self, speed):
        if speed >= 0:
            self.dir1.low()
            self.dir2.high()
        else:
            self.dir1.high()
            self.dir2.low()
        self.speed = abs(speed)
        self.pwm.duty_u16(int(self.speed * 65535 / 100))

    def stop(self):
        self.dir1.low()
        self.dir2.low()
        self.pwm.duty_u16(0)

# roller dc motor
pwm_pin = 27
dc_dir_pin1 = 26
dc_dir_pin2 = 28
bldc_motor = BLDCMotor(pwm_pin, dc_dir_pin1, dc_dir_pin2)

while True:
    print("neg direction")
    bldc_motor.set_speed(-100)
    utime.sleep(5)
    print("stop")
    bldc_motor.stop()
    utime.sleep(2)
    print("pos direction")
    bldc_motor.set_speed(100)
    utime.sleep(5)
    print("stop")
    bldc_motor.stop()
    utime.sleep(2)


