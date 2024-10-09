# Known problems: 
#     mAs system gets the correct angles needed to move arm after
#     being moved once already. But still thinks that the arm is a 0,0,0 
#     before moving the arm for a second time

import utime
from machine import Pin
import math

#Joint 1(a1)
pinA1 = Pin(8, Pin.OUT)
pinB1 = Pin(9, Pin.OUT)
pinC1 = Pin(10, Pin.OUT)
pinD1 = Pin(11, Pin.OUT)

Pins1 = [pinA1, pinB1, pinC1, pinD1]

#Joint 2(a2)
pinA2 = Pin(12, Pin.OUT)
pinB2 = Pin(13, Pin.OUT)
pinC2 = Pin(14, Pin.OUT)
pinD2 = Pin(15, Pin.OUT)
Pins2 = [pinA2, pinB2, pinC2, pinD2]

#Base(b)
pinA3 = Pin(4, Pin.OUT)
pinB3 = Pin(5, Pin.OUT)
pinC3 = Pin(6, Pin.OUT)
pinD3 = Pin(7, Pin.OUT)
Pins3 = [pinA3, pinB3, pinC3, pinD3]

FULL = [[1,0,0,1],
        [1,1,0,0],
        [0,1,1,0],
        [0,0,1,1]]
HALF = [[1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]]
FULL_REVERSED = [[1,0,0,1],
                [0,0,1,1],
                [0,1,1,0],
                [1,1,0,0]]
HALF_REVERSED = [[1,0,0,1],
                [0,0,0,1],
                [0,0,1,1],
                [0,0,1,0],
                [0,1,1,0],
                [0,1,0,0],
                [1,1,0,0],
                [1,0,0,0]]

DELAY = 2
steps = 0
initSteps = 0
w = 48 #Robotic Arm Length(Both)
bcA = 0
a1cA = 0
a2cA = 0
cAs = (bcA, a1cA, a2cA)


def moveToPos(x,y,z,phaseMode,DELAY,Pins1,Pins2,Pins3,cAs):
    mAs = (0,0,0)
    Pins = [Pins1, Pins2, Pins3]
    b = math.atan2(y,x)*(180/3.1415) #Base Angle
    l = math.sqrt(x*x + y*y) #X and Y Extension
    h = math.sqrt(l*l + z*z)
    phi = math.atan(z/l)*(180/3.1415)
    theta = math.acos((h/2)/w)*(180/3.1415)
    a1 = phi + theta
    a2 = phi - theta
    
    #Round all the numbers to nearest integer
    b = math.floor(b)
    a1 = math.floor(a1)
    a2 = math.floor(a2)
    #Inverse a2 angle(May need to remove this when testing the arm)
    if (a2 < 0):
        a2 = abs(a2)
        
    
    tAs = (b, a1, a2)
    print("tAs: ", tAs)
    #Base mA
    if(b < 0 and cAs[0] < 0):
        bmA = (abs(cAs[0] - b))
    elif(b < 0):
        bmA = -(abs(cAs[0] - b))
    else:
        bmA = (abs(cAs[0] - b))
        
    #a1 mA
    if(a1 < 0 and cAs[1] < 0):
        a1mA = (abs(cAs[1] - a1))
    elif(a1 < 0):
        a1mA = -(abs(cAs[1] - a1))
    else:
        a1mA = (abs(cAs[1] - a1))
        
    #a2 mA
    if(a2 < 0 and cAs[2] < 0):
        a2mA = (abs(cAs[2] - a2))
    elif(a2 < 0):
        a2mA = -(abs(cAs[2] - a2))
    else:
        a2mA = (abs(cAs[2] - a2))
    
    mAs = (bmA, a1mA, a2mA)
    
    print("mAs: ", mAs)
    reallyMoveToAngleAll(b,a1,a2,phaseMode,DELAY,Pins,mAs)
    return (mAs)

def reallyMoveToAngleAll(b,a1,a2,phaseMode,DELAY,Pins,tAs):
    running = True
    bSteps = 0
    a1Steps = 0
    a2Steps = 0
    bDone = False
    a1Done = False
    a2Done = False
    bPhases = 0
    a1Phases = 0
    a2Phases = 0
    while(running):
        for i in phaseMode:
            for y in Pins:
                for x, pin in enumerate(y):
                    
                    if(bDone != True and y == Pins[2]):
                        pin.value(i[x])
                        bPhases += 1
                    if(a1Done != True and y == Pins[0]):
                        pin.value(i[x])
                        a1Phases += 1
                    if(a2Done != True and y == Pins[1]):
                        pin.value(i[x])
                        a2Phases += 1
                    utime.sleep_ms(1)
        if(bDone != True):
            bSteps += 1
        if(a1Done != True):
            a1Steps += 1
        if(a2Done != True):
            a2Steps += 1
            
        if(bSteps >= math.ceil(b*1.42222222)):
            bDone = True
        if(a1Steps >= math.ceil(a1*1.42222222)):
            a1Done = True
        if(a2Steps >= math.ceil(a2*1.42222222)):
            a2Done = True
                
        #print("bSteps: ", bSteps, b, math.ceil(b*1.42222222), bDone)
        #print("a1Steps: ", a1Steps, a1, math.ceil(a1*1.42222222), a1Done)
        #print("a2Steps: ", a2Steps, a2, math.ceil(a2*1.42222222), a2Done)
        running = not(bDone and a1Done and a2Done)
    
        
    
def moveToAngleAll(b,a1,a2,phaseMode,DELAY,Pins1,Pins2,Pins3):
    #print("Before:")
    moveToAngleBase(b, Pins3,phaseMode,DELAY)
    #print("After Base:")
    moveToAngleA1(a1, Pins1,phaseMode,DELAY)
    #print("After A1:")
    moveToAngleA2(a2, Pins2,phaseMode,DELAY)
    #print("After A2:")   
def moveToAngleBase(b, Pins, phaseMode, DELAY):
    #print("Base Angle: ", b)
    s=0
    for y in range(math.ceil(b*1.42222222)):
        for i in phaseMode:
            for x,pin in enumerate(Pins):
                #print("Base")
                #pin.value(i[x])
                #utime.sleep_ms(DELAY)
                p=0
                s += 1
    print("bSteps: ", s/16)
def moveToAngleA1(a1, Pins, phaseMode, DELAY):
    #print("A1 Angle: ", a1)
    s=0
    for y in range(math.ceil(a1*1.42222222)):
        for i in phaseMode:
            for x,pin in enumerate(Pins):
                #print("A1")
                #pin.value(i[x])
                #utime.sleep_ms(DELAY)
                p=0
                s += 1
    print("a1Steps: ", s/16)
def moveToAngleA2(a2, Pins, phaseMode, DELAY):
    #print("A2 Angle: ", a2)
    s=0
    for y in range(math.ceil(a2*1.42222222)):
        for i in phaseMode:
            for x,pin in enumerate(Pins):
                #print("A2")
                #pin.value(i[x])
                #utime.sleep_ms(DELAY)
                p=0
                s += 1
    print("a2Steps: ", s/16)
    
while True:
    try:
        print("Enter 1001 to Quit")
        X = int(input("Enter X coordinate: "))
        Y = int(input("Enter Y coordinate: "))
        Z = int(input("Enter Z coordinate: "))
        #phaseMode = input("Enter Phase Mode(FULL/HALF/FULL_REVERSED/HALF_REVERSED): ")
        
        
        if ((X or Y or Z) == 1001):
            break
        else:
            #Pins = [Pins1, Pins2, Pins3]
            #reallyMoveToAngleAll(X,Y,Z,FULL,DELAY,Pins)
            
            
            print("Before:", cAs)
            cAs = moveToPos(X,Y,Z,FULL,DELAY,Pins1,Pins2,Pins3, cAs)
            print("After: ",cAs)
            #Reverse direction 
            
            #moveToPos(X,Y,Z,FULL_REVERSED,DELAY,Pins1,Pins2,Pins3,cAs)
            
            
        
        
    except KeyboardInterrupt:
        
        pinA1.low()
        pinB1.low()
        pinC1.low()
        pinD1.low()
        pinA2.low()
        pinB2.low()
        pinC2.low()
        pinD2.low()
        pinA3.low()
        pinB3.low()
        pinC3.low()
        pinD3.low()
        break
