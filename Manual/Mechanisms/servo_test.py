from servo import Servo
gate_servo_pin = 17
gate_servo = Servo(gate_servo_pin)
deg = (50 * 1024)/180
gate_servo.goto(deg)