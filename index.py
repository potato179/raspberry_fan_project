import RPi.GPIO as GPIO
import time

# GPIO 7개 GPIO Pin 번호 설정
#               A  B  C  D  E  F  G
segment_pins = [15, 23, 24, 25, 13, 7, 12]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for segment in segment_pins:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

# Common Anode일 경우 : LOW -> LED ON, HIGH -> LED OFF
# Common Cathod일 경우 : LOW -> LED OFF, HIGH -> LED ON
# data = [0, 0, 0, 0, 0, 0, 1]
data = [[1, 1, 1, 1, 1, 1, 0],  #0
        [0, 1, 1, 0, 0, 0, 0],  #1
        [1, 1, 0, 1, 1, 0, 1],  #2
        [1, 1, 1, 1, 0, 0, 1],  #3
        [0, 1, 1, 0, 0, 1, 1],  #4
        [1, 0, 1, 1, 0, 1, 1],  #5
        [1, 0, 1, 1, 1, 1, 1],  #6
        [1, 1, 1, 0, 0, 0, 0],  #7
        [1, 1, 1, 1, 1, 1, 1],  #8
        [1, 1, 1, 0, 0, 1, 1]]  #9

try:
    for i in range(10):
        for j in range(len(segment_pins)):
            GPIO.output(segment_pins[j], data[i][j])
        time.sleep(1)
finally:
    GPIO.cleanup()
    print("게이조이고")