import imp
from nntplib import GroupInfo
import time
import cv2
import RPI.GPIO as GPIO

print("석현게이설")

SEGMENT_PINS = [2, 3, 4, 5, 6, 7, 8]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# https://rydepier.wordpress.com/2016/05/30/l9110-fan-motor-keyes-board/