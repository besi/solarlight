import neopixel
import machine
import time

# ADC
from machine import ADC
adc = ADC(0)

# initialize I2C display
#from machine import Pin, I2C
#import ssd1306
#i2c = I2C(sda=Pin(4), scl=Pin(5))
#display = ssd1306.SSD1306_I2C(128, 60, i2c)

reset_pin = 16
reset = machine.Pin(reset_pin, machine.Pin.OUT)
reset.value(1)

mode = 0
mode_count = 6
mode_pin = 0
mode_button = machine.Pin(mode_pin, machine.Pin.IN, machine.Pin.PULL_UP)

neopixel_pin = 2
led_count = 5
np = neopixel.NeoPixel(machine.Pin(neopixel_pin), led_count)

def rainbow(led_count):
    # Rainbow code by https://wokwi.com/arduino/projects/305569065545499202

    rainbow = [
      (126 , 1 , 0),(114 , 13 , 0),(102 , 25 , 0),(90 , 37 , 0),(78 , 49 , 0),(66 , 61 , 0),(54 , 73 , 0),(42 , 85 , 0),
      (30 , 97 , 0),(18 , 109 , 0),(6 , 121 , 0),(0 , 122 , 5),(0 , 110 , 17),(0 , 98 , 29),(0 , 86 , 41),(0 , 74 , 53),
      (0 , 62 , 65),(0 , 50 , 77),(0 , 38 , 89),(0 , 26 , 101),(0 , 14 , 113),(0 , 2 , 125),(9 , 0 , 118),(21 , 0 , 106),
      (33 , 0 , 94),(45 , 0 , 82),(57 , 0 , 70),(69 , 0 , 58),(81 , 0 , 46),(93 , 0 , 34),(105 , 0 , 22),(117 , 0 , 10)]

    while True:
        rainbow = rainbow[-1:] + rainbow[:-1]
        for i in range(led_count):
            np[i] = rainbow[i]
            np.write()
        
        time.sleep_ms(100)

def read_battery():
    value = str(adc.read())
    print(value)
    #display.fill(0)
    #display.text('Voltage: ' + value, 0, 0, 1)
    #display.show()


def mode_changed(event):
    global mode, modes
    mode = mode + 1
    mode = mode % (mode_count + 1)
    print("new mode: " + str(mode))
    if mode == 1:
        read_battery()
    elif mode == 2:
        np.fill((255, 255, 255))
    elif mode == 3:
        np.fill((0, 0, 255))
    elif mode == 4:
        np.fill((255, 0, 0))
    elif mode == 5:
        np.fill((0, 255, 0))
    elif mode == 6:
        rainbow(led_count)
    np.write()
    time.sleep(1)

mode_button.irq(trigger=machine.Pin.IRQ_FALLING, handler=mode_changed)


def clear(): 
    np.fill((0, 0, 0))
    np.write()

def fivecolors():
    np[0] = (18,50,250)
    np[1] = (180,50,0)
    np[2] = (180,50,255)
    np[3] = (18,250,25)
    np[4] = (218,50,25)
    np.write()

fivecolors()
#rainbow(led_count)
