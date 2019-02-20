#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
import os
os.system('setfont Lat15-TerminusBold14')

ml = LargeMotor('outA')
mr = LargeMotor('outD')
claw = MediumMotor('outB')


touch = TouchSensor('in2')

us = UltrasonicSensor('in3')

cl = ColorSensor('in1')
cr = ColorSensor('in4')

us.mode="US-DIST-CM"

cl.mode="RGB-RAW"
cr.mode="RGB-RAW"

btn = Button()

# Variables




find = []

encoder = 0

# Bracketing Constant
kb = 5

# Sensitivity
sens = 0
errorlast = 0

gsens = 8

# Sensors

linel = [45, 380]
liner = [43, 380]



greenl = [87, 200]
greenr = [80, 207]



silverl = 500

silverr = 500


# P
kp = 0.9

tp = 200

# I

ki = 0.14

integral = 0

# D

kd = 0.25

lasterror = 0

derivative = 0

# Functions

def can_find():
    while us.value() > 300:
        ml.run_forever(speed_sp=50)
        mr.run_forever(speed_sp=-50)

    ml.stop(stop_action='hold')
    mr.stop(stop_action='hold')

    time.sleep(0.25)

#    while us.value() > 300:
#        ml.run_to_rel_pos(position_sp=1, speed_sp=400, stop_action='hold')
#        mr.run_to_rel_pos(position_sp=-1, speed_sp=400, stop_action='hold')





    

    edge = us.value() + 1

    if edge > 300:
        edge = 300

    print(edge)



    while us.value() < edge:

        ml.run_to_rel_pos(position_sp=3, speed_sp=100, stop_action='hold')
        mr.run_to_rel_pos(position_sp=-3, speed_sp=100, stop_action='hold')

        ml.wait_while('running')
        mr.wait_while('running')  

        time.sleep(0.2)

        find.append(us.value())
        
        

    # Process everything because otherwise it fails

    short = [0, 9999, 0]


    for x in range(len(find)):
        process = find[x]

        print(process)

        if process < short[1]:
            short = [x + 1, process, 0]

    x = 0
    i = 0

    for x in range(len(find)):
        process2 = find[x]

        if process2 == short[1]:
            i = i + 1

    short[2] = i

    print('')
    print(short[2])
    print('')






    turnBack = (len(find) - short[0] - (short[2] / 2)) * 3

    print(len(find), ' ', short[0], ' ', turnBack, ' ', short[1])

    ml.run_to_rel_pos(position_sp=-turnBack, speed_sp=100, stop_action='hold')
    mr.run_to_rel_pos(position_sp=turnBack, speed_sp=100, stop_action='hold')

    ml.wait_while('running')
    mr.wait_while('running')

    dist = short[1]

    # Amazing Maths
    trav = (dist / 110 * 360)
    encoder = ml.position

    if trav > 600:
        trav = 600

    print(trav)

    # Move to the Can
    ml.run_to_rel_pos(position_sp=-trav, speed_sp=1000, stop_action='hold')
    mr.run_to_rel_pos(position_sp=-trav, speed_sp=1000, stop_action='hold')

    ml.wait_while('running')
    mr.wait_while('running')

    # Grab it
    claw.run_timed(time_sp=500, speed_sp=1000, stop_action='coast')

    claw.wait_while('running')

    rest = 600 - trav

    # Push it Out
    ml.run_to_rel_pos(position_sp=-rest, speed_sp=1000, stop_action='hold')
    mr.run_to_rel_pos(position_sp=-rest, speed_sp=1000, stop_action='hold')

    ml.wait_while('running')
    mr.wait_while('running')

    # Let it go
    claw.run_timed(time_sp=500, speed_sp=-1000, stop_action='coast')

    claw.wait_while('running')

    # Come Back
    ml.run_to_rel_pos(position_sp=600, speed_sp=1000, stop_action='hold')
    mr.run_to_rel_pos(position_sp=600, speed_sp=1000, stop_action='hold')

    ml.wait_while('running')
    mr.wait_while('running')




def can():
    # Can Function

    # Go to the middle

    ml.run_to_rel_pos(position_sp=1000, speed_sp=800, stop_action='hold')
    mr.run_to_rel_pos(position_sp=1000, speed_sp=1000, stop_action='hold')

    ml.wait_while('running')
    mr.wait_while('running')

    ml.reset()

    # Find the Can
    can_find()

    # Turn Back
#    if encoder < 1100:
#        ml.position = encoder

    while ml.position < 400:
        ml.run_forever(speed_sp=300)
        mr.run_forever(speed_sp=-300)

#    if encoder > 1100
#        ml.position = encoder

    while ml.position > 400:
        ml.run_forever(speed_sp=-300)
        mr.run_forever(speed_sp=300)

    ml.stop(stop_action='hold')
    mr.stop(stop_action='hold')

    while cl.value(0) < 100:
        ml.run_forever(speed_sp=1000)
        mr.run_forever(speed_sp=1000)

    ml.stop(stop_action='hold')
    mr.stop(stop_action='hold')

    ml.wait_while('running')
    mr.wait_while('running')

    while cl.value(0) < 100:
        ml.run_forever(speed_sp=200)
        mr.run_forever(speed_sp=200)

    ml.stop(stop_action='hold')
    mr.stop(stop_action='hold')

    ml.run_to_rel_pos(position_sp=100, speed_sp=550, stop_action='hold')
    mr.run_to_rel_pos(position_sp=100, speed_sp=1000, stop_action='hold')

    ml.wait_while('running')
    mr.wait_while('running')




# Amazing Calibration UI

print('Calibrate?')
print('Left = No, Right = Yes')

while not btn.left and not btn.right:
    time.sleep(0.01)

print('')
print('')
print('')
print('')
print('')
print('')
print('')
print('')
print('')
print('')

if btn.right:
    print('Press Dowm To Calibrate Black')
    while not btn.down:
        print('Left:', cl.value(0), end='  ')
        print('Right:', cr.value(0))
        time.sleep(1)
    linel[0] = cl.value(0)
    liner[0] = cr.value(0)

    time.sleep(0.5)
    
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    
    print('Press Up To Calibrate White')
    while not btn.up:
        print('Left:', cl.value(0), end='  ')
        print('Right:', cr.value(0))
        time.sleep(1)
    linel[1] = cl.value(0)
    liner[1] = cr.value(0)

    time.sleep(0.5)

    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    
    print('Press Left To Calibrate Green Left')
    while not btn.left:
        print('Left:', cl.value(1))
        time.sleep(1)
    greenl[0] = cl.value(0)
    greenl[1] = cr.value(1)

    time.sleep(0.5)

    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    
    print('Press Right To Calibrate Green Right')
    while not btn.right:
        print('Right:', cl.value(1))
        time.sleep(1)
    greenr[0] = cr.value(0)
    greenr[1] = cr.value(1)

    time.sleep(0.5)

# Final Sensor Calibration

lmid = (linel[0] + linel[1]) / 2

rmid = (liner[0] + liner[1]) / 2

turnl = [greenl[0] + 10, greenl[1] - gsens, greenl[1] + gsens]
turnr = [greenr[0] + 10, greenr[1] - gsens, greenr[1] + gsens]



greenlt = [greenl[1] + gsens, greenl[1] - gsens, greenl[0] + gsens]
greenrt = [greenr[1] + gsens, greenr[1] - gsens, greenr[0] + gsens]



print('')
print('')
print('')
print('')
print('')
print('')
print('')
print('')
print('')
print('Press Down To Begin')

while not btn.down:
    time.sleep(0.01)

print('')
print('')
print('')
print('')
print('')
print('')
print('')
print('')
print('')



while True:
    # Get all Colour Sensor Values
    rl = cl.value(0)
    rr = cr.value(0)


    # Bracket Sensor Values
    valL = rl
    valR = rr

    if valL < linel[0]:
        valL = linel[0]
    if valL > linel[1]:
        valL = linel[1]
    
    if valR < liner[0]:
        valR = liner[0]
    if valR > liner[1]:
        valR = liner[1]

    # Center Sensor Values
    centl = valL - lmid
    centr = valR - rmid

    # Lineralise
    errorl = (centl / lmid) * 100
    errorr = (centr / rmid) * 100

    # Calculate Error
    error = errorl + (errorr * -1)


    # Ignore Small Changes
#    if error < errorlast - sens or error > errorlast + sens:
#        errorlast = error
#    else:
#        error = errorlast



    # PID Loop

    integral = integral + error

    if error < 5 and error > -5:
        integral = 0

    if btn.enter:
        integral = 0

    if integral > 1000:
        integral = 1000
    
    if integral < -1000:
        integral = -1000

    derivative  = error - lasterror

    turn = kp * error + ki * integral + kd * derivative

    pl = tp + turn
    pr = tp - turn

    if pl > 1000:
        pl = 1000
    if pl < -1000:
        pl = -1000

    if pr > 1000:
        pr = 1000
    if pr < -1000:
        pr = -1000



    ml.run_forever(speed_sp=pl)
    mr.run_forever(speed_sp=pr)

    lasterror = error

    if btn.down:
        integral = 0
    
    

    
    gl = cl.value(1)
    gr = cr.value(1)

    rl = cl.value(0)
    rr = cr.value(0)



    if gl < greenlt[0] and gl > greenlt[1] and gr < greenlt[2]:

        print("turning")

        ml.stop(stop_action='hold')
        mr.stop(stop_action='hold')

        mr.run_to_rel_pos(position_sp=295, speed_sp=400, stop_action="hold")
        ml.run_to_rel_pos(position_sp=100, speed_sp=400, stop_action="hold")
        mr.wait_while("running")

        integral = 0

    if gr < greenrt[0] and gr > greenrt[1] and rr < greenrt[2]:

        print("turning")

        ml.stop(stop_action='hold')
        mr.stop(stop_action='hold')

        ml.run_to_rel_pos(position_sp=295, speed_sp=400, stop_action="hold")
        mr.run_to_rel_pos(position_sp=100, speed_sp=400, stop_action="hold")
        ml.wait_while("running")

        integral = 0
    
    if cl.value(0) > silverl:
        while cr.value(0) < silverr:
            mr.run_to_rel_pos(position_sp=1, speed_sp=400, stop_action="hold")
        can()
    
    if cr.value(0) > silverr:
        while cl.value(0) < silverl:
            ml.run_to_rel_pos(position_sp=1, speed_sp=400, stop_action="hold")
        can()


    if touch.value() == 1:
        ml.stop(stop_action='hold')
        mr.stop(stop_action='hold')

        mr.run_to_rel_pos(position_sp=-400, speed_sp=1000, stop_action='hold')
        ml.run_to_rel_pos(position_sp=-100, speed_sp=1000, stop_action='hold')

        mr.wait_while('running')
        ml.wait_while('running')

        ml.run_forever(speed_sp=350)
        mr.run_forever(speed_sp=500)

        time.sleep(2)

        ml.run_forever(speed_sp=370)
        mr.run_forever(speed_sp=600)

        while(cr.value(0) > liner[0] + 10):
            time.sleep(0.01)
        
        ml.stop(stop_action='hold')
        mr.stop(stop_action='hold')
        
        ml.run_to_rel_pos(position_sp=200, speed_sp=1000, stop_action='hold')

        ml.wait_while('running')