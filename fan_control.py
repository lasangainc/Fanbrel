import RPi.GPIO as GPIO
import time
import os

FAN_PIN = 14  # GPIO14 (BCM)
ON_TEMP = 60  # degrees Celsius
OFF_TEMP = 50  # degrees Celsius

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)
fan_on = False

def get_temp():
    # Reads CPU temperature from system file
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp_str = f.readline()
        return int(temp_str) / 1000.0  # convert to Celsius

try:
    while True:
        temp = get_temp()
        if temp >= ON_TEMP and not fan_on:
            GPIO.output(FAN_PIN, GPIO.HIGH)
            fan_on = True
        elif temp <= OFF_TEMP and fan_on:
            GPIO.output(FAN_PIN, GPIO.LOW)
            fan_on = False
        time.sleep(5)  # check every 5 seconds
except KeyboardInterrupt:
    pass
finally:
    GPIO.output(FAN_PIN, GPIO.LOW)
    GPIO.cleanup()
