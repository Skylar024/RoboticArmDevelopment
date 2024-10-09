import utime
#import motorController
from machine import Pin
import math

# buttonCW = Pin(17, Pin.IN)
# buttonCCW = Pin(16, Pin.IN)
# buttonQuit = Pin(18, Pin.IN)

'''Initialize Pins'''
pinA1 = Pin(8, Pin.OUT)
pinB1 = Pin(9, Pin.OUT)
pinC1 = Pin(10, Pin.OUT)
pinD1 = Pin(11, Pin.OUT)
Pins1 = [pinA1, pinB1, pinC1, pinD1]

pinA2 = Pin(12, Pin.OUT)
pinB2 = Pin(13, Pin.OUT)
pinC2 = Pin(14, Pin.OUT)
pinD2 = Pin(15, Pin.OUT)
Pins2 = [pinA2, pinB2, pinC2, pinD2]

pinA3 = Pin(4, Pin.OUT)
pinB3 = Pin(5, Pin.OUT)
pinC3 = Pin(6, Pin.OUT)
pinD3 = Pin(7, Pin.OUT)
Pins3 = [pinA3, pinB3, pinC3, pinD3]

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
        direction = input('Enter a Direction(CW/CCW/X): ')
        if direction == 'cw':
            print("Spinning Clock-Wise")
            rotateCW(PinGroupList, DELAY, max_steps)
            #utime.sleep_ms(2)
        if direction == 'ccw':
            print("Spinning CounterClock-Wise")
            rotateCCW(PinGroupList, DELAY, max_steps)
            #utime.sleep_ms(2)
        
        if direction == 'x':
            print("Ending Program")
            break
        
    except KeyboardInterrupt:
        break
