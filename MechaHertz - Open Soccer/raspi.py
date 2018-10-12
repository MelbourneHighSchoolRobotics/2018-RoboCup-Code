# Owen:
#
# Code should be pretty much up to date with what we used on the day (nationals).
# Other versions exist that have capability for goal detection, but we didn't find that feasible on the day.
# Essentially, we set things up by declaring our ranges, setting up the camera and opening serial.
# Then, each loop, we flip the frame, change it to HSV, develop the mask, draw a circle around the largest section.
# We then send the center point of that circle to the arduino as a percentage. The arduino chooses actions.
# If we find a ValueError, it indicates that there are not pixels matching our colour range.
# In this case, we count it in offscreencount, and if we have 100 frames (~5s) without seeing the ball
# we admit we're lost and tell the arduino.
# Finally, we clean up the frame. 
# All of the commented code is to provide visuals or qol improvements for human people.
#
# Side note: there are 18 spaces in this program, so evidently, I do use spaces.

import cv2 #image processing
from serial import Serial #communication
from picamera import PiCamera #interface with pi camera
from picamera.array import PiRGBArray #create cv2 style frames

framewidth=320; frameheight=240
lower=(160,90,60); upper=(190,255,190) #calibrated ball bounds

#initialise piCamera
camera=PiCamera()
camera.resolution=(framewidth,frameheight)
camera.framerate=32
rawCapture=PiRGBArray(camera,size=(framewidth,frameheight))

ser=Serial('/dev/ttyS0',115200,timeout=.01)

offscreencount=0 #how many frames has it been since we saw the ball

#we use a for loop to iterate through the frames received from the camera.
for image in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    frame=cv2.flip(image.array,-1) #our camera was upside down
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #turn our video from RGB to HSV
    mask=cv2.inRange(frame,lower,upper) #filter frame for pixels in range
    im2,contours,hierarchy=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #define countours (witchcraft)
    try:
        c=max(contours,key=cv2.contourArea) #get dimensions of contours
        (x,y),radius=cv2.minEnclosingCircle(c) #draw circle around space defined
        xc=int(round((x/framewidth)*100,0)); yc=int(round((y/frameheight)*100,0)) #determine position of ball as percentage        
        ser.write(b'b%sx%sy' % (str(xc).encode(),str(yc).encode())) #write to serial

        # cv2.circle(frame,(int(x),int(y)),int(radius),(255,0,0),3) #draw a circle around the ball
        # cv2.putText(frame,"%s, %s" % (xc,yc),(10,465),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),4) #write the coords of the ball on the frame
        # print("%s, %s" & (str(xc),str(yc))) #print out the coords opf the ball
    except ValueError: #if we get a value error, its because there is nothing matching our inrange
        # print("off screen") 
        offscreencount+=1
        if offscreencount>=100:
            ser.write(b'l') #l means we are lost, as we haven't seen the ball for some time
            offscreencount=0


    #cv2.imshow('image',frame)
    rawCapture.truncate(0) #get rid of spent frame
    
    #if keyboard inputs 'q', close all windows and end the program
    # key=cv2.waitKey(1) & 0xFF
    # if key==ord('q'):
    #     cv2.destroyAllWindows()
    #     break