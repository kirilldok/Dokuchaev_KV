import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac    = [8, 11, 7, 1, 0, 5, 12, 6]
comp   = 21
troyka = 13

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = 1)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    for value in range(256):
        dec_val = decimal2binary(value)
        GPIO.output(dac, dec_val)
        comp_val = GPIO.input(comp)
        time.sleep(0.01)
        if ( comp_val == 1):
            return value
    return 0

try:
    while True:
            results = adc()
            print(results)
            voltage = (results / 256) * 3.3
            print(f' Напряжение =  {voltage:.2f}V')

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()

