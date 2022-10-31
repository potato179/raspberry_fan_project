'''

        #  # #### #### #   #  ##  #### #### #   #
       #  # #  # #    ##  # #    #     ##  ##  #
      #### #### #### # # # # ## ####  ##  # # #
     #  # #  # #    #  ## #  #    #  ##  #  ##
    #  # #  # #### #   #  ##  #### #### #   #

'''

import imp
import RPi.GPIO as GPIO
import time
import spidev

spi = spidev.SpiDev()
# SPI 통신 시작
spi.open(0, 0)  # bus:0, dev:0 (CE0:0, CE1:1)
# SPI 통신 속도 설정
spi.max_speed_hz = 100000
print("석현게이설")

buzzer_pin = 2
button_pin = 14
switch_input_pin = 26
led_red_pin = 21
led_green_pin = 20
led_blue_pin = 16
segment_pins = [15, 23, 24, 25, 13, 7, 12]
fan_vcc_pin = 4
PWM_pin = 5

cnt = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(switch_input_pin, GPIO.IN)
GPIO.setup(led_red_pin, GPIO.OUT)
GPIO.setup(led_green_pin, GPIO.OUT)
GPIO.setup(led_blue_pin, GPIO.OUT)
GPIO.setup(PWM_pin, GPIO.OUT)

pwm = GPIO.PWM(PWM_pin, 100000)
pwm.start(0)

for segment in segment_pins:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
# Common Anode일 경우 : LOW -> LED ON, HIGH -> LED OFF
# Common Cathod일 경우 : LOW -> LED OFF, HIGH -> LED ON
# data = [0, 0, 0, 0, 0, 0, 1]
data = [
    [1, 1, 1, 1, 1, 1, 0], #0
    [0, 1, 1, 0, 0, 0, 0], #1
    [1, 1, 0, 1, 1, 0, 1], #2
    [1, 1, 1, 1, 0, 0, 1], #3
    [0, 1, 1, 0, 0, 1, 1], #4
    [1, 0, 1, 1, 0, 1, 1], #5
    [1, 0, 1, 1, 1, 1, 1], #6
    [1, 1, 1, 0, 0, 0, 0], #7
    [1, 1, 1, 1, 1, 1, 1], #8
    [1, 1, 1, 0, 0, 1, 1] #9
]

def analog_read(channel):
    ret = spi.xfer2([1, (8 + channel)<<4, 0])
    adc_out = ((ret[1] & 3) << 8) + ret[2]
    return adc_out

def print_7seg(gab):
    for i in range(len(segment_pins)):
        GPIO.output(segment_pins[i], data[gab][i])

while True:
    # 0번 채널에서 읽어온 SPI 데이터(0~1023)
    reading = analog_read(0)
    #reading = random.randrange(0,1024)
    # 전압수치로 변환
    voltage = reading * 5 / 1023
    print_7seg(int(reading/103))
    
    if int(reading/103)*10 == 0:
        pwm.stop()
        print(int(reading/103)*10)
    elif int(reading/103)*10 == 1:
        pwm.start(10)
        print("ok start")

    else: 
        pwm.ChangeDutyCycle(int(reading/103)*10 + 5)
        print("ok going")

    if int(reading/103) == 0:
        GPIO.output(led_red_pin, GPIO.LOW)
        GPIO.output(led_green_pin, GPIO.HIGH)
        GPIO.output(led_blue_pin, GPIO.HIGH)
    else:
        if GPIO.input(switch_input_pin):
            GPIO.output(led_red_pin, GPIO.HIGH)
            GPIO.output(led_green_pin, GPIO.LOW)
            GPIO.output(led_blue_pin, GPIO.HIGH)
        else:
            GPIO.output(led_red_pin, GPIO.HIGH)
            GPIO.output(led_green_pin, GPIO.HIGH)
            GPIO.output(led_blue_pin, GPIO.LOW)

    if int(reading/103) == 1:
        if cnt == 0:
            cnt = 1
            GPIO.output(buzzer_pin, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(buzzer_pin, GPIO.LOW)