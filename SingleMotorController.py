import utime
#import motorController
from machine import Pin
import math

buttonCW = Pin(17, Pin.IN)
buttonCCW = Pin(16, Pin.IN)
buttonQuit = Pin(18, Pin.IN)

pinA = Pin(12, Pin.OUT)
pinB = Pin(13, Pin.OUT)
pinC = Pin(14, Pin.OUT)
pinD = Pin(15, Pin.OUT)
Pins = [pinA, pinB, pinC, pinD]

NINE = [1,0,0,1]
TWELVE = [1,1,0,0]
SIX = [0,1,1,0]
THREE = [0,0,1,1]
sequence = [NINE, TWELVE, SIX, THREE]    

degrees = int(input("Enter degrees to turn: "))

initSteps = 0
DELAY = 2
steps = 0
max_steps = math.ceil(degrees * 1.42222222)
# 360° = 512
# 180° = 256
# 90° = 128

def rotateCW(Pins, delay, num_of_steps):
    steps = 0
    for x in range(num_of_steps):
        pinA.high()
        pinB.low()
        pinC.low()
        pinD.high()
        utime.sleep_ms(delay)
            
        pinA.high()
        pinB.high()
        pinC.low()
        pinD.low()
        utime.sleep_ms(delay)
            
        pinA.low()
        pinB.high()
        pinC.high()
        pinD.low()
        utime.sleep_ms(delay)
            
        pinA.low()
        pinB.low()
        pinC.high()
        pinD.high()
        utime.sleep_ms(delay)
    
        steps += 1
        #print(steps)
    
    pinA.low()
    pinB.low()
    pinC.low()
    pinD.low()

def rotateCCW(Pins, delay, num_of_steps):
    steps = 0
    for x in range(num_of_steps):
        pinA.low()
        pinB.low()
        pinC.high()
        pinD.high()
        utime.sleep_ms(delay)
        
        pinA.low()
        pinB.high()
        pinC.high()
        pinD.low()
        utime.sleep_ms(delay)
        
        pinA.high()
        pinB.high()
        pinC.low()
        pinD.low()
        utime.sleep_ms(delay)
        
        pinA.high()
        pinB.low()
        pinC.low()
        pinD.high()
        utime.sleep_ms(delay)
        
        steps += 1
        #print(steps)
    
    pinA.low()
    pinB.low()
    pinC.low()
    pinD.low()
            

while True:
    try:
        if buttonCW.value() == 0:
            print("Spinning Clock-Wise")
            rotateCW(Pins, DELAY, max_steps)
            utime.sleep_ms(2)
        if buttonCCW.value() == 0:
            print("Spinning CounterClock-Wise")
            rotateCCW(Pins, DELAY, max_steps)
            utime.sleep_ms(2)
        
        if buttonQuit.value() == 0:
            print("Ending Program")
            break
        
    except KeyboardInterrupt:
        
        
        pinA.low() #0 
        pinB.low() #0
        pinC.low() #0
        pinD.low() #0
        break
