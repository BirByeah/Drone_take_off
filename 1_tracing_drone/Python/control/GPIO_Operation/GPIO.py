import RPi.GPIO as GPIO
import time

pin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
pwm1 = GPIO.PWM(pin, 30)
pwm1.start(0)
while True:
    for dc in range(0, 100, 5):
        pwm1.ChangeDutyCycle(dc)
        time.sleep(0.05)