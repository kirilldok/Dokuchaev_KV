import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

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

dac=[8, 11, 7, 1, 0, 5, 12, 6]
leds=[2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13
maxV = 3.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(leds, GPIO.OUT, initial=GPIO.LOW)

voltaged = []
timed = []

try:
    start = time.time()
    GPIO.output(troyka, GPIO.HIGH)
    i = 0
    while i < 200:
        i = adc()
        GPIO.output(leds, perev(i))
        print("вольты", i/256 * 3.3)
        voltaged.append(i/256*3.3)
        timed.append(time.time() - start)

    GPIO.output(troyka, GPIO.LOW)

    while i > 180:
        i = adc()
        print("Вольты", i/256*3.3)
        GPIO.output(leds, perev(i))
        voltaged.append(i/256*3.3)
        timed.append(time.time() - start)

    end = time.time()

    with open("settings.txt", "w") as file:
        file.write(str((end-start)/len(voltaged)))
        file.write("\n")
        file.write(str(maxV/256))

    print("Продолжительность: ", (end - start))
    print("Период измерения:", (end-start)/len(voltaged)) 
    print("частота дискретизации: ", len(voltaged) / (end-start)) 
    print("шаг квантования АЦП: ", maxV/256)

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()


timed_str = [str(i) for i in timed]
voltaged_str = [str(i) for i in voltaged]

with open("data_V.txt", "w") as file:
    file.write("\n".join(voltaged_str))
with open("data_T.txt", "w") as file:
    file.write("\n".join(timed_str))

plt.plot(timed, voltaged)
plt.show()

