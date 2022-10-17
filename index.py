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
segment_pins = [15, 23, 24, 25, 21, 7, 12]
fan_vcc_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(switch_input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_red_pin, GPIO.OUT)
GPIO.setup(led_green_pin, GPIO.OUT)
GPIO.setup(led_blue_pin, GPIO.OUT)
for segment in segment_pins:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
GPIO.setup(fan_vcc_pin, GPIO.OUT)
GPIO.setwarnings(False)
# switch를 켰을 때  카메라 on 상태
# 상시로 가변저항 값 읽고 7 segments에 0~9 단위로 띄우기
# 7세그 값 하나 올라갈 때 마다 부저 삑소리 올라감
# RGB LED 켜졌을 때는 초록색 꺼졌을 때는 빨간색
# 잠깐만
# 버튼 누르면 소리하고 불빛 다 꺼 (야간모드)
while True:

# https://rydepier.wordpress.com/2016/05/30/l9110-fan-motor-keyes-board/