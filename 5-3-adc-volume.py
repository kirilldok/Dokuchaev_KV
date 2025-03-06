import RPi.GPIO as GPIO
import time


dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 21
troyka = 13


GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=1)
GPIO.setup(comp, GPIO.IN)

def perev(a):
    return [int (elem) for elem in bin(a)[2:].zfill(8)]

def adc():
    k = 0
    for i in range(7, -1, -1):
        k+= 2**i
        dac_val = perev(k)
        GPIO.output(dac, dac_val)
        time.sleep(0.01)
        comp_val = GPIO.input(comp)
        if comp_val:
            k -= 2**i
    return k

leds = [2,3,4,17,27,22,10,9]
GPIO.setup(leds,GPIO.OUT)

def light_up(voltage):
    numled= int(voltage/3.3 *8)
    for i in range(8):
        if i<numled:
            GPIO.output(leds[i],1)
        else:
            GPIO.output(leds[i],0)
try:
    while True:
        value = adc()  
        voltage = (value / 256.0) * 3.3 
        print(f"Напряжение: {voltage:.2f}V")
        light_up(voltage)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
