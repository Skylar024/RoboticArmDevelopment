import utime
#import motorController
from machine import Pin
import math

buttonCW = Pin(17, Pin.IN)
buttonCCW = Pin(16, Pin.IN)
buttonQuit = Pin(18, Pin.IN)

'''Initialize Pins'''
pin1A = Pin(12, Pin.OUT)
pin1B = Pin(13, Pin.OUT)
pin1C = Pin(14, Pin.OUT)
pin1D = Pin(15, Pin.OUT)
Pins1 = [pin1A, pin1B, pin1C, pin1D]

pin2A = Pin(8, Pin.OUT)
pin2B = Pin(9, Pin.OUT)
pin2C = Pin(10, Pin.OUT)
pin2D = Pin(11, Pin.OUT)
Pins2 = [pin2A, pin2B, pin2C, pin2D]

pin3A = Pin(4, Pin.OUT)
pin3B = Pin(5, Pin.OUT)
pin3C = Pin(6, Pin.OUT)
pin3D = Pin(7, Pin.OUT)
Pins3 = [pin3A, pin3B, pin3C, pin3D]

PinGroupList = [Pins1, Pins2, Pins3]
'''Initialize Pins'''


'''Initialize Stepper Motor Phase Sequence'''
NINE = [1,0,0,1]
TWELVE = [1,1,0,0]
SIX = [0,1,1,0]
THREE = [0,0,1,1]
sequence = [NINE, TWELVE, SIX, THREE]
'''Initialize Stepper Motor Phase Sequence'''   

degrees = int(input("Enter degrees to turn: "))

initSteps = 0
DELAY = 2 #Delay set to 10ms because multiple motors in sequence get faster(this is to prevent motor chain from spinning into itself)
steps = 0
max_steps = math.ceil(degrees * 1.42222222)
# 360° = 512
# 180° = 256
# 90° = 128

def rotateCW(listOfPinGroups, delay, numOfSteps):
    steps = 0
    for i in range(numOfSteps):
        for x in listOfPinGroups:
            x[0].high()
            x[1].low()
            x[2].low()
            x[3].high()
            utime.sleep_ms(delay)
                
            x[0].high()
            x[1].high()
            x[2].low()
            x[3].low()
            utime.sleep_ms(delay)
                
            x[0].low()
            x[1].high()
            x[2].high()
            x[3].low()
            utime.sleep_ms(delay)
                
            x[0].low()
            x[1].low()
            x[2].high()
            x[3].high()
            utime.sleep_ms(delay)
        steps += 1
        print(steps)

def rotateCCW(listOfPinGroups, delay, numOfSteps):
    steps = 0
    for i in range(numOfSteps):
        for x in listOfPinGroups:
            x[0].low()
            x[1].low()
            x[2].high()
            x[3].high()
            utime.sleep_ms(delay)
            
            x[0].low()
            x[1].high()
            x[2].high()
            x[3].low()
            utime.sleep_ms(delay)
            
            x[0].high()
            x[1].high()
            x[2].low()
            x[3].low()
            utime.sleep_ms(delay)
            
            x[0].high()
            x[1].low()
            x[2].low()
            x[3].high()
            utime.sleep_ms(delay)
        steps += 1
        print(steps)
            

while True:
    try:
        if buttonCW.value() == 0:
            print("Spinning Clock-Wise")
            rotateCW(PinGroupList, DELAY, max_steps)
            utime.sleep_ms(2)
        if buttonCCW.value() == 0:
            print("Spinning CounterClock-Wise")
            rotateCCW(PinGroupList, DELAY, max_steps)
            utime.sleep_ms(2)
        
        if buttonQuit.value() == 0:
            print("Ending Program")
            break
        
    except KeyboardInterrupt:
        break
