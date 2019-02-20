#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time
import sys

#The front of the robot (ball capturing zone) is on a *edge*
#Ultrasonic on left, ir back and  , motors clockwise from (top being the ball capturing zone and the front of the robot) top right, a, b, c, d and when all moving forward, the robot moves forward
#compass can be anywhere, doesn't matter as long as it is away from interferance

#Initialises all the Externally connected objects and variables
#initialises Motors
MotorA = ev3.LargeMotor("outA")
MotorB = ev3.LargeMotor("outB")
MotorC = ev3.LargeMotor("outC")
MotorD = ev3.LargeMotor("outD")
button = ev3.Button()
#initialises IR sensors
IR_back = ev3.Sensor("in4", driver_name = "ht-nxt-ir-seek-v2")
IR_front = ev3.Sensor("in2", driver_name = "ht-nxt-ir-seek-v2")
#Sets modes for IR sensors
IR_front.mode = 'AC-ALL'
IR_back.mode = 'AC-ALL'
#initialises and sets up Compass sensors
Compass = ev3.Sensor("in3", driver_name = "ht-nxt-compass")
Compass.mode = "COMPASS"
#initialises and sets up Ultrasonic sensors
US = ev3.UltrasonicSensor("in1")
US.mode = "US-DIST-CM"
#initialises the buttons on the Ev3
button = ev3.Button()
#Finds the current distance bettween the US and the wall - the robot will now take this value, 'US_goal', as the distance that the Ultrasonic must reach to be facing the goal
US_goal = US.value(0)
#This is just to take the current Compass value (0 - 359) and assign it to a value to be definied as the 'goal-heading', or the way that it needs to face to face the goals that we need to score in.
Goal_Heading = Compass.value(0)
#This is to initialise and tell the program that default for the main loop is in unpaused mode
Paused = False

def Relative_Heading(Absolute, Goal_Heading):
    #Minuses Goal_Heading from the Absolute heading, therefore 'shifting' the whole 'spectrum' of values down by Goal_Heading, eg. making abs heading 20, and goal heading of 20, the output is 0, if abs heading is 0 instead, output is -20
    Absolute -= Goal_Heading
    #Make All negative values positive, by shifting all of them back \p, eg. with a goal heading of 20, and abs heading of 0, that would result in -20 above - here it would be converted into 340, if abs was 19, the stuff above would output -1, and when coming here, it would be turned into 359.
    if Absolute < 0:
        Absolute += 360
    #Here it turns all of the positive values above into neg and positive values. All numbers greater than 180 are on the left side of the compass, if we do, heading - 360, if we have 359, that would be made appropiately into -1, while 181 would be made into -179 appropiately
    if Absolute > 180:
        Absolute = Absolute - 360
    # print(Absolute, "HI", Compass.value())
    return Absolute
PastHeading = 0
def Sub_Driver(A, B, C, D, speed, MoveType):
    global Goal_Heading
    global PastHeading
    Heading = Relative_Heading(Compass.value(), Goal_Heading)
    # if ((PastHeading - 30) > Heading) or ((PastHeading + 30) < Heading):
    #     Heading = PastHeading
    #     print("Boo")
    # PastHeading = Heading
    if MoveType == 0:
        if Heading < 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round((abs(MotorC.speed) + abs(MotorD.speed)) / 2)) / speed
            A = A * Heading * AverageMultiplier
            B = B * Heading * AverageMultiplier
        elif Heading > 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round((abs(MotorA.speed) + abs(MotorB.speed)) / 2)) / speed
            C = C * Heading * AverageMultiplier
            D = D * Heading * AverageMultiplier
    elif MoveType == 1:
        if Heading < 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round((abs(MotorA.speed) + abs(MotorB.speed)) / 2)) / speed
            D = D * Heading * AverageMultiplier
            C = C * Heading * AverageMultiplier
        elif Heading > 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round((abs(MotorC.speed) + abs(MotorD.speed)) / 2)) / speed
            A = A * Heading * AverageMultiplier
            B = B * Heading * AverageMultiplier
    elif MoveType == 2:
        if Heading < 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round((abs(MotorA.speed) + abs(MotorD.speed)) / 2)) / speed
            C = C * Heading * AverageMultiplier
            B = B * Heading * AverageMultiplier
        elif Heading > 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round((abs(MotorB.speed) + abs(MotorC.speed)) / 2)) / speed
            A = A * Heading * AverageMultiplier
            D = D * Heading * AverageMultiplier
    elif MoveType == 3:
        if Heading < 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round((abs(MotorB.speed) + abs(MotorC.speed)) / 2)) / speed
            A = A * Heading * AverageMultiplier
            D = D * Heading * AverageMultiplier
        elif Heading > 0:
            Heading = abs(Heading /  179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round((abs(MotorA.speed) + abs(MotorD.speed)) / 2)) / speed
            C = C * Heading * AverageMultiplier
            B = B * Heading * AverageMultiplier
    #Pass into diagonals
    if MoveType == 4: 
        if Heading < 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round(abs(MotorD.speed))) / speed
            B = B * Heading * AverageMultiplier
        elif Heading > 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round(abs(MotorB.speed))) / speed
            D = D * Heading * AverageMultiplier
    elif MoveType == 5:
        if Heading < 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round(abs(MotorA.speed))) / speed
            C = C * Heading * AverageMultiplier
        elif Heading > 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round(abs(MotorC.speed))) / speed
            A = A * Heading * AverageMultiplier
    elif MoveType == 6:
        if Heading < 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round(abs(MotorB.speed))) / speed
            D = D * Heading * AverageMultiplier
        elif Heading > 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round(abs(MotorD.speed))) / speed
            B = B * Heading * AverageMultiplier
    elif MoveType == 7:
        if Heading < 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round(abs(MotorC.speed))) / speed
            A = A * Heading * AverageMultiplier
        elif Heading > 0:
            Heading = abs(Heading / 179)
            if Heading > 1:
                Heading = 1
            Heading = 1 - Heading
            AverageMultiplier = (round(abs(MotorA.speed))) / speed
            C = C * Heading * AverageMultiplier
    elif MoveType == 8:
        AverageMultiplier = (round((abs(MotorD.speed) + abs(MotorB.speed)) / 2)) / 1000
        A = A * AverageMultiplier
        C = C * AverageMultiplier
    elif MoveType == 9:
        AverageMultiplier = (round((abs(MotorA.speed) + abs(MotorC.speed)) / 2)) / 1000
        B = B * AverageMultiplier
        D = D * AverageMultiplier
        
    # elif MoveType == 8:
        # if Heading < 0:
        #     Heading = abs(Heading / 179)
        #     if Heading > 1:
        #         Heading = 1
        #     Heading = 1 - Heading
        #     AverageMultiplier = (round(abs(MotorD.speed))) / speed
        #     B = B *8 Heading * AverageMultiplier
            # AverageMultiplier = (round(abs(MotorC.speed))) / speed
            # A = A * Heading * AverageMultiplier
        # elif Heading > 0:
        #     Heading = abs(Heading / 179)
        #     if Heading > 1:
        #         Heading = 1
        #     Heading = 1 - Heading
        #     AverageMultiplier = (round(abs(MotorB.speed))) / speed
        #     D = D * Heading * AverageMultiplier
            # AverageMultiplier = (round(abs(MotorA.speed))) / speed
            # C = C * Heading * AverageMultiplier
    # elif MoveType == 9:
    #     if Heading < 0:
    #         Heading = abs(Heading / 179)
    #         if Heading > 1:
    #             Heading = 1
    #         Heading = 1 - Heading
    #         AverageMultiplier = (round(abs(MotorC.speed))) / speed
    #         A = A * Heading * AverageMultiplier
            # AverageMultiplier = (round(abs(MotorD.speed))) / speed
            # B = B * Heading * AverageMultiplier
        # elif Heading > 0:
        #     Heading = abs(Heading / 179)
        #     if Heading > 1:
        #         Heading = 1
        #     Heading = 1 - Heading
        #     AverageMultiplier = (round(abs(MotorA.speed))) / speed
        #     C = C * Heading * AverageMultiplier
            # AverageMultiplier = (round(abs(MotorB.speed))) / speed
            # D = D * Heading * AverageMultiplier
    if A == 0:
        MotorA.stop()
    else:
        MotorA.run_forever(speed_sp = speed * A * -1, stop_action = "brake")
    if B == 0:
        MotorB.stop()
    else:
        MotorB.run_forever(speed_sp = speed * B * -1, stop_action = "brake")
    if C == 0:
        MotorC.stop()
    else:
        MotorC.run_forever(speed_sp = speed * C, stop_action = "brake")
    if D == 0:
        MotorD.stop()
    else:
        MotorD.run_forever(speed_sp = speed * D, stop_action = "brake")

#Receives instructions in a simplified format and decodes them for Sub Driver
def Driver(Dir, speed):
    if speed == 0: #Stop All Motors (I'm using speed now as it is easier to decode that)
        Sub_Driver(0, 0, 0, 0, speed, 10)
    elif Dir == 0: #Move Forward (Run All Motors Forward) N
        Sub_Driver(1, 1, 1, 1, speed, 0)
    elif Dir == 45: #Move Top right NE
        Sub_Driver(0, 1, 0, 1, speed, 4)
    elif Dir == 90: #Move right E
        Sub_Driver(-1, 1, -1, 1, speed, 2)
    elif Dir == 135: #Move bottom right SE
        Sub_Driver(-1, 0, -1, 0, speed, 5)
    elif Dir == 180 or Dir == -180: #Move down S
        Sub_Driver(-1, -1, -1 , -1, speed, 1) 
    elif Dir == -135: #Move bottom left SW
        Sub_Driver(0, -1, 0, -1, speed, 6)
    elif Dir == -90: #Move left W
        Sub_Driver(1, -1, 1, -1, speed, 3)
    elif Dir == -45: #Move top left NW
        Sub_Driver(1, 0, 1, 0, speed, 7)
    else:
        raise ValueError("Driver num invalid - Check to make sure that dir is a valid direction, or if speed for stop is == 0")

def MoveToBall():
    IRback = IR_back.value(0)
    IRfront = IR_front.value(0)
    IRfrontList = [IR_front.value(1), IR_front.value(2), IR_front.value(3), IR_front.value(4), IR_front.value(5)]
    IRbackList = [IR_back.value(1), IR_back.value(2), IR_back.value(3), IR_back.value(4), IR_back.value(5)]
    if max(IRfrontList) > max(IRbackList):
        if 1 <IRfront < 9:
            IRfront -= 5
            IRfront *= 45
            Driver(IRfront, 1000)
        elif IRback == 5:
            if US_goal > US.value():
                Driver(-90, 1000)
            else:
                Driver(90, 1000)
        elif (1 < IRback < 9):
            Driver(180, 1000)
        elif (IRback == 9) or (IRfront == 1):
            Driver(-135, 1000)
        elif (IRback == 1) or (IRfront == 9):
            Driver(135, 1000)
        else:
            Driver(180, 1000)
    else:
        if IRback == 5:
            if US_goal > US.value():
                Driver(-90, 1000)
            else:
                Driver(90, 1000)
        elif (1 < IRback < 9):
            Driver(180, 1000)
        elif (IRback == 9) or (IRfront == 1):
            Driver(-135, 1000)
        elif (IRback == 1) or (IRfront == 9):
            Driver(135, 1000)
        elif 1 <IRfront < 9:
            IRfront -= 5
            IRfront *= 45
            Driver(IRfront, 1000)
        else:
            Driver(180, 1000)

PastValueIR = 0
IRfade = 0
PreviousReturnValue = False
USFirstMove = False
def BallCaptured():
    global IRfade
    global PastValueIR
    global PreviousReturnValue
    global USFirstMove
    if (abs(PastValueIR - (IR_front.value(1) + IR_front.value(2) + IR_front.value(3) + IR_front.value(4) + IR_front.value(5)))) > 130:
        IRfade = time.time() + 0.75 
    PastValueIR = (IR_front.value(1) + IR_front.value(2) + IR_front.value(3) + IR_front.value(4) + IR_front.value(5))
    if IRfade >= time.time():
        if PreviousReturnValue == False:
            # TimeTrack = time.time() + 0.5
            # while time.time() <= TimeTrack:
            #     Driver(0, 1000)
            USFirstMove = True
        PreviousReturnValue = True
        return True
    else:
        USFirstMove = False
        PreviousReturnValue = False
        return False

def BallCapturedMovement():
    global US_goal
    global USFirstMove
    USvalue = US.value()
    if USFirstMove == True:
        if (US_goal + 150) < USvalue:
            Driver(-45, 1000)
        elif (US_goal - 250) > USvalue:
            Driver(45, 1000)
        else:
            USFirstMove = False
            Driver(0, 1000)
    else:
        Driver(0, 1000)

print("Press button to start")
while True:
    if button.enter == True:
        while button.enter == True:
            pass
        IRfade = time.time() + 3
        break
print("Program starting")

#Main program starts
while True:
    #pause function - Changes the paused variable to the opposite boolean, it then keeps it here until the button is let go so that it doesn't activate multiple times with 1 press
    if button.enter == True:
        if Paused == True:
            #sets paused to false if already true
            Paused = False
            #Holds the program until the button press has finished - to not run this multiple times.
            while button.enter == True:
                pass
                IRfade = time.time() + 3
            print("Now running")
        elif Paused == False:
            #sets paused to True if already False
            Paused = True
            #Holds the program until the button press has finished - to run this multiple times.
            while button.enter == True:
                pass
            print("Paused")
    #checks if the program is supposed to be paused.
    if Paused == False:
        try:
            #stage 0, Getting the ball
            if BallCaptured() == True:
                BallCapturedMovement()
            else:
                MoveToBall()
        #print(IR_front.value(1), IR_front.value(2), IR_front.value(3), IR_front.value(4), IR_front.value(5))
        #Sub_Driver(0.2, 1, 0.2, 1, 1000, 8)
        #Driver(0, 300)
        except:
            print("Error - Something went wrong")
    else:
        Driver(0, 0) #Stops all Motors when it is paused.