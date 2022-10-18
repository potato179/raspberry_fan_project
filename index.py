import imp
from nntplib import GroupInfo
import spidev
import time
import cv2
import RPi.GPIO as GPIO

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
GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(switch_input_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(led_red_pin, GPIO.OUT)
GPIO.setup(led_green_pin, GPIO.OUT)
GPIO.setup(led_blue_pin, GPIO.OUT)
for segment in segment_pins:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
GPIO.setup(fan_vcc_pin, GPIO.OUT)
GPIO.setwarnings(False)
# SPI 인스턴스 생성
spi = spidev.SpiDev()
# SPI 통신 시작
spi.open(0, 0)  # bus:0, dev:0 (CE0:0, CE1:1)
# SPI 통신 속도 설정
spi.max_speed_hz = 100000
# switch를 켰을 때  카메라 on 상태
# 상시로 가변저항 값 읽고 7 segments에 0~9 단위로 띄우기
# 7세그 값 하나 올라갈 때 마다 부저 삑소리 올라감
# RGB LED 켜졌을 때는 초록색 꺼졌을 때는 빨간색
# 잠깐만
# 버튼 누르면 소리하고 불빛 다 꺼 (야간모드)
# https://rydepier.wordpress.com/2016/05/30/l9110-fan-motor-keyes-board/
try:
    while True:
        if GPIO.input(switch_input_pin):
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            cap = cv2.VideoCapture(0)

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.resize(frame, (400,300))
                # gray스케일 이미지로 변환
                #img = cv2.imread(frame)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # 이미지에서 얼굴 검출
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                # 얼굴 위치에 대한 좌표 정보 가져오기
                for (x, y, w, h) in faces:
                    # 원본이미지에 얼굴 위치 표시
                    # (x,y) 에서 시작, 끝점(x+가로), (y+세로), BGR색, 굵기 2
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
                    if(x):
                        print("True")
                    else:
                        print("False")

                cv2.imshow('img', frame)
                if cv2.waitKey(10) == 27:
                    break

        # 0~7까지 8개의 채널에서 SPI 데이터 읽기
        def analog_read(channel):
            ret = spi.xfer2([1, (8 + channel)<<4, 0])
            adc_out = ((ret[1] & 3) << 8) + ret[2]
            return adc_out

        while True:
            # 0번 채널에서 읽어온 SPI 데이터(0~1023)
            reading = analog_read(0)
            #reading = random.randrange(0,1024)
            # 전압수치로 변환
            voltage = reading * 3.3 / 1023
            print("Reading=%d, voltage=%f" % (reading, voltage))

finally:
    cap.release()
    cv2.destroyAllWindows()
    spi.close()













































































































































































































    