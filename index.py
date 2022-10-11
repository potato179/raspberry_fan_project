import imp
from nntplib import GroupInfo
import time
import cv2
import RPI.GPIO as GPIO

print("석현게이설")

buzzer_pin = 2
button_pin = 14
switch_input_pin = 26
led_red_pin = 21
led_green_pin = 20
led_blue_pin = 16
segment_pins = [15, 23, 24, 25, 8, 7, 12]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# https://rydepier.wordpress.com/2016/05/30/l9110-fan-motor-keyes-board/

