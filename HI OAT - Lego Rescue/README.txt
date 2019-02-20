in order to run this program, ev3dev must be installed with python.

Ports:

1: left colour sensor
2: touch sensor
3: ultrasonic sensor
4: right colour sensor

A: Left drive motor (Large)
B: Claw motor (Medium)
C:
D: Right drive motor (Large)

touch sensor, ultrasonic sensor and claw must be connected for the program to run, however, they do not need to be mounted for linefollowing.

Can Function:

1- robot moves into the middle of the spill zone
2- robot starts rotating clockwise until it sees the left edge of the can
3- robot takes a measurement of the distance to the edge of the can (Used to find the other edge)
4- robot takes periodic distance measurements and appends them to an array until it sees the right edge of the can
5- robot processes this array to find the point where the can was closest to the robot (if more than one of these points     exists, the robot finds the middle point)
6- robot takes the distance to the can and converts it to degrees
7- robot moves up to the can and grabs it
8- robot moves the rest of the way out of the spill zone and releases the can
9- robot moves back to the center of the spill zone
10- if the robot has circled less than 180 degrees, the robot continues to turn to the 180 point so the front is facing towards the silver tape. if the robot has passed this point, it turns back
11- robot moves forward until it is off the green
12- robot resumes line following


Line following:

1- take readings of red reflectivity
2- bracket values so they are only what we expect
3- center values (subtract the average of top and bottom values: 0 to 100 becomes -50 to 50
4- place current value on a scale of -100 to 100 from the scale it was at before
5- use both sensor values to produce a single error value
6- if error is small, reset integral
7- cap the integral to stop it getting very high
8- calculate derivative
9- calculate difference in motor powers
10- add difference to base motor power
11- cap motor powers at -1000 to 1000 to stop them going crazy
12- assign motor powers


Green Turns:

1- if reflectivity of green is inside a bracket and reflectivity of red is below a specific threshold, the sensor has hit green
2- stop motors
3- curve to the side of the sensor so in the end, the sensors will be on both sides of the line
4- reset the integral so it is as if its restarting linefollowing


Silver:

1- if one sensor hits silver, move toe other sensor forward until it hits silver so it sort of straightens up


Water Tower:

1- if touch sensor has been pressed,
2- stop motors
3- curve backwards to move away from the water tower and become perpendicular to it
4- do a wide curve
5- wait 2 seconds and then do a sharper curve
6- wait until the right sensor sees black
7- straighten up



Robot Design:

the general design of the robot was a generic two wheeled robot. in the rear, we added two omni wheels in order to create space in the center for the virtical ultrasonic sensor. the ultrasonic sensor is mounted vertially to reduce the horisontal distance it sees to make it more accurate in finding the can.

as this robot was made in a few days, there are many improvements that could be made. the choice of tyres over treads was made because going downhill with treads failed. the issue with tyres is lack of traction. a solution to this is to use weights over the tyres which we ended up doing. the downside of this was the robot became very front heavy and it would tip forward sometimes. a better idea would be to build two drive bases and only use the one with tyres if we were going downhill on the course, otherwise, use the robot with treads. another solution would be to use larger or wider wheels in order to create 

the claw design was a hoop that flipped over the robot. while great for saving space, it meant the can had to be more or less perfectly alligned in order to be captured. a better way of doing this would be to use a traditional claw that flips out of the side or the robot rather than being mounted behind it. this way, it stays out of the way and does not need the can to be perfectly alligned.

when using colour sensors, it is very important to keep the sensors at the same height above the ground at all times as if this is not done, reflectivity can vary as they move up or down relative to the ground, as would happen with inclines or speed bumps. one solution to this is to have the sensors very close to the wheels, however, this makes programming difficult as the sensors don't 'slide' accross the floor. a solution to this is to build a sensor mount seperate from the robot with slides and mount it using a 4 bar system to the robot so it can move up and down seperate from the robot but won't fall over.

the reason we didn't use the ultrasonic to look for the water tower is because the ultrasonic has a minimum visible distance that we found to be ~8cm. if any object comes within 8cm of the robot, it would go around it. if the can was plaed just after the silver tape, the robot would see the can before the silver tape and go around it. this is also why our touch sensor was mounted above the height of the can.