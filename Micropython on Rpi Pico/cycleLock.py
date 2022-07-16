import time
from machine import Pin, PWM

#Setting minimum and maximum pwm duty cycle. Changes with the servo model.
MIN_DUTY = 1500
MAX_DUTY = 8300

servo = PWM(Pin(0))
servo.freq(50)

angle = MIN_DUTY
direction = 100

while True:
    if angle == MIN_DUTY:
        direction = +100
    elif angle == MAX_DUTY:
        direction = -100
    angle = angle + direction
    print("Moving to ", angle)
    servo.duty_u16(angle)
    time.sleep(0.01)
