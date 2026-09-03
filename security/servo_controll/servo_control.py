from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18, min_angle=0, max_angle=180)

def open_box():
    print("Opening box")
    servo.angle = 90
    sleep(5)

def close_box():
    print("Closing box")
    servo.angle = 0
    sleep(1)
