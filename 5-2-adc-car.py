import RPi.GPIO as GPIO
from time import sleep

dac=[8, 11, 7, 1, 0, 5, 12, 6]
comp = 21
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)


def perev(a):
    return [int (elem) for elem in bin(a)[2:].zfill(8)]

def adc():
    k = 0
    for i in range(7, -1, -1):
        k+= 2**i
        dac_val = perev(k)
        GPIO.output(dac, dac_val)
        sleep(0.01)
        comp_val = GPIO.input(comp)
        if comp_val:
            k -= 2**i
    return k

try:
    while (True):
        i = adc()
        voltage = i*3.3/256.0
        if i: print("{:.2f}".format(voltage))
    
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()