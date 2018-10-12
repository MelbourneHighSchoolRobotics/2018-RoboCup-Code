# MechaHertz Open Soccer MHS Robotics

Design

Our robot used a four wheel, 3 layer design, with a dribbler.
It used a raspberry pi and picam for vision which communicated over serial to an Arduino Mega for power control and decision making.
The motors where powered 2 to an H-Bridge, with a third H-Bridge used to power the dribbler.

Our software solution was to use opencv image analysis on the raspberry pi, which sent coordinates and a few special characters to the arduino.
The arduino would then process this input and make decisions about movement, dribbling, etc.

More detailed comments on software can be found in the appropriate files.


Notes and thoughts:


Hardware
    Four wheels offered no real benefit, as we placed the dribbler and camera between 2 wheels and used this as the front.
    Five threaded rods was more stability than necessary, and made taking layers off more of an annoyance.
    Camera solution that allows us to see both near and far easily and reliably. Probably on bottom plate.
    Our robot could only see ~70% of the field.
    We had issues with ensuring consistent power supply between layers.
    The acrylic plates used were fragile and prone to breaking.
    Using a breadboard with wires everywhere was both confusing, making maintenance harder, and easy to disrupt.
    The middle plate of the design was highly innacessible, which was awkward as it held most of the things for which access was needed.
    It would have been better to fully design the robot prior to construction.
    Much more testing was necessary, as simple ~15 minute fix problems cost us games when they should have been caught earlier.


Software
    We needed to have a full robot assembled long before we did, so we could develop and test on it.
    Because of this, the Arduino program was underdeveloped, although the opencv stuff worked fine.
    I'm unsure that it makes any sense to use HSV colour, given that the ball and goals are fairly similar in this space and quite different in RGB.
    Probably good to teach people to use SSH over Ethernet through Bonjour or some other solution, as WiFi is not a working solution at nationals.
