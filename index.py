import RPi.GPIO as GPIO
import time
import spidev
import cv2

# spi 변수 선언
spi = spidev.SpiDev()
# SPI 통신 시작
spi.open(0, 0)  # bus:0, dev:0
# SPI 통신 속도 설정
spi.max_speed_hz = 100000

# GPIO 핀번호 설정
buzzer_pin = 2
button_pin = 14
switch_input_pin = 26
led_red_pin = 21
led_green_pin = 20
led_blue_pin = 16
segment_pins = [15, 23, 24, 25, 13, 7, 12]
PWM_pin = 19

# 사용될 변수 선언
buzzer_cnt = 0 # 
led_cnt = 0 # 
dnd_cnt = 1 # 야간보드 버튼 변수
nm = 1 # 야간모드 변수
int_reading = 0 # 아날로그 값 한자리수로

# GPIO세팅
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # 풀다운 저항 기능
GPIO.setup(switch_input_pin, GPIO.IN)
GPIO.setup(led_red_pin, GPIO.OUT)
GPIO.setup(led_green_pin, GPIO.OUT)
GPIO.setup(led_blue_pin, GPIO.OUT)
GPIO.setup(PWM_pin, GPIO.OUT)
# 7segment GPIO세팅
for segment in segment_pins:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

# pwm세팅
pwm = GPIO.PWM(PWM_pin, 100)
pwm.start(0)

# 7segment에 표시할 숫자 설정
data = [
    [1, 1, 1, 1, 1, 1, 0], # 0
    [0, 1, 1, 0, 0, 0, 0], # 1
    [1, 1, 0, 1, 1, 0, 1], # 2
    [1, 1, 1, 1, 0, 0, 1], # 3
    [0, 1, 1, 0, 0, 1, 1], # 4
    [1, 0, 1, 1, 0, 1, 1], # 5
    [1, 0, 1, 1, 1, 1, 1], # 6
    [1, 1, 1, 0, 0, 0, 0], # 7
    [1, 1, 1, 1, 1, 1, 1], # 8
    [1, 1, 1, 0, 0, 1, 1], # 9
    [0, 0, 0, 0, 0, 0, 0] # 야간모드
]

# xml 분류기 파일 로그(카메라 얼굴 인식 기능)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# 카메라 장치 열기
cap = cv2.VideoCapture(0)

# 아날로그 신호 읽는 함수
def analog_read(channel):
    ret = spi.xfer2([1, (8 + channel)<<4, 0])
    adc_out = ((ret[1] & 3) << 8) + ret[2]
    return adc_out

# 7segment에 숫자 표시하는 함수
def print_7seg(gab):
    for i in range(len(segment_pins)):
        GPIO.output(segment_pins[i], data[gab][i])

# 얼굴에 사각형 그려서 화면에 띄우는 함수
def face_rectengle():
     # 얼굴 위치에 대한 좌표 정보 가져오기
    for (x, y, w, h) in faces:
        # 원본이미지에 얼굴 위치 표시
        # (x,y) 에서 시작, 끝점(x+가로), (y+세로), BGR색, 굵기 2
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("img", frame)
    if cv2.waitKey(10) == 27:
        print("end")

# 빨간 LED 켜는 함수
def red_on():
    GPIO.output(led_red_pin, GPIO.LOW)
    GPIO.output(led_green_pin, GPIO.HIGH)
    GPIO.output(led_blue_pin, GPIO.HIGH)

# 파란 LED 켜는 함수
def blue_on():
    GPIO.output(led_red_pin, GPIO.HIGH)
    GPIO.output(led_green_pin, GPIO.HIGH)
    GPIO.output(led_blue_pin, GPIO.LOW)

# 초록 LED 켜는 함수
def green_on():
    GPIO.output(led_red_pin, GPIO.HIGH)
    GPIO.output(led_green_pin, GPIO.LOW)
    GPIO.output(led_blue_pin, GPIO.HIGH)

# LED 끄는 함수
def led_off():
    GPIO.output(led_red_pin, GPIO.HIGH)
    GPIO.output(led_green_pin, GPIO.HIGH)
    GPIO.output(led_blue_pin, GPIO.HIGH)

# 팬모터 pwm 제어 함수
def pwmm():
    if int_reading == 0:
        pwm.ChangeDutyCycle(0)
    elif int_reading == 1:
        pwm.ChangeDutyCycle(10)
    else: 
        pwm.ChangeDutyCycle(int_reading*10+10)
    print("mcp %d" %int_reading)

# 피에조 부저 울리는 함수
def buzzer_beep():
    GPIO.output(buzzer_pin, GPIO.HIGH) # 부져 켜기
    time.sleep(0.12) # 0.12초 쉬고
    GPIO.output(buzzer_pin, GPIO.LOW)  # 부져 끄기

a = 0

# 프로그램 실행을 위한 무한 반복문
try:
    while True:

        #시간을 올리는 함수
        print(a)
        a+=1

        # 이미지 읽기
        ret, frame = cap.read()

        # 입력 안됨 알림
        if not ret:
            print("camera no signal")

        # 입력받은 이미지 크기 재설정
        frame = cv2.resize(frame, (400,300))

        # gray스케일 이미지로 변환
            # img = cv2.imread(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 이미지에서 얼굴 검출
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # length가 0이면 감지 안된거
        print("face: %d" %len(faces))

        # 얼굴 인식 여부 확인
        if(len(faces)):
            print("face O")
        else:
            print("face X")

        # 얼굴에 사각형 그려 띄우기
        face_rectengle()

        # pwm 설정
        pwmm()

        # 아날로그 신호 읽어오기
        reading = analog_read(0)
        int_reading = int(reading/103)   # 0~1023을 103으로 나눴을 때, 0~9 사이값이 나옴
            # test
        print("int_reading: %d" %int_reading)

        # 야간 모드 확인
        # nm = night_mode(dnd_cnt)
        # 야간 모드 버튼 클릭 여부 확인
        # dnd_cnt가 0이면 야간모드, 1이면 일반모드
        if GPIO.input(button_pin):
            # print(dnd_cnt) 
            if dnd_cnt == 1:
                dnd_cnt = 0
                # return 1
            else:
                dnd_cnt = 1
                # return 0
        time.sleep(0.2)   # 입력 시간을 늘려서 오류 방지

        if dnd_cnt == 1: # 야간 모드가 아닐 때
            # 7segment에 fan세기 띄우기
            print_7seg(int_reading)

            # 조건문(LED) 해석: 야간모드가 꺼있을 때 만약 fan 세기가 0이라면 항상 빨강, 세기가 1이상일 때 카메라가 켜있으면 초록색, 꺼있으면 파란색. 야간모드라면 불 꺼짐
            if int_reading == 0: # 팬이 꺼져있을 때 빨간 불 켜기
                red_on()
            else: # 아니라면
                if GPIO.input(switch_input_pin): # 카메라 스위치가 켜있을 때 초록불
                    green_on()
                else: # 카메라 꺼있으면 파란불
                    blue_on()

            # 조건문(buzzer) 해석: 팬이 꺼져있다가 켜지거나, 켜저있다가 꺼지면 소리가 남
            if int_reading == 1: # 팬 세기가 1이라면
                if buzzer_cnt == 0: # 부져가 0이라면
                    buzzer_cnt = 1 # 부져를 1로 바꾸고
                    buzzer_beep()

            elif int_reading == 0: # 아니고 만약 팬세기가 0이라면
                if buzzer_cnt == 1: # 부저가 1이라면
                    buzzer_cnt = 0 # 부져를 0으로 바꾸고
                    buzzer_beep()

            # 조건문(switch) 해석: 스위치카 꺼지거나 켜질 때 소리 내고, LED변수 값을 바꿔서 LED색 제어할 수 있도록 함
            if GPIO.input(switch_input_pin): # 스위치가 켜지면
                if led_cnt == 0: # led 값이 0이면
                    led_cnt = 1 # led 1로 바꾸고
                    buzzer_beep()
            else:
                if led_cnt == 1: # led 값이 1이면
                    led_cnt = 0 # led 0으로 바꾸고
                    buzzer_beep()
        
        else:   # 야간모드 켜질 시 LED모두 꺼짐 및 소리 모두 꺼짐
            led_off()
            print_7seg(10) # 7segment 끄기

        print(" ")

finally:
    cap.release()
    cv2.destroyAllWindows()
    spi.close()
    GPIO.cleanup()