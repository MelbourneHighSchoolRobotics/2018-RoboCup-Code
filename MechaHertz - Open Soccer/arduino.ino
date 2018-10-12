#include "RB_Motor.h"

/*
Owen:

I couldn't find an up-to-date version of the code, but I implemented most of the changes we made to the code on the day.

Essentially, each loop we check whether there is input from the button, and if there is, we change whether we want to keep moving.
Then, if we do want to keep running, we check if there is serial input. If there is, we process it and make movement decisions.
Movement decisions come down to: if ball is in front of us, charge it. If it's to the left or right, turn toward it.
If it's close to us, charge it. If we're charging, the dribbler is running.
*/

char inChar; //most recent character from Serial
String inStr; //current input recorded from serial
int bx,by; //ball's position
int g1x,g1y; //position of a goal
int g2x,g2y; //postion of other goal 
int *xpos,*ypos; //used to reference a set of coordinates
bool go=false; //should we be moving?
int btn; //used to hold input from the start button

Motor motorFrontLeft(8,9,100);
Motor motorFrontRight(6,7,100);
Motor motorBackLeft(2,3,100);
Motor motorBackRight(4,5,100);

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN,OUTPUT); //used to show where the arduino thinks the ball is
  pinMode(21,INPUT); //used for the button input
}

void loop() {
  btn=digitalRead(21);
  if (btn==LOW){
    //btn is LOW when pressed. When it is pressed, we switch whether the bot is  on
    go=!(go);
    delay(300);
  }
  if (go){
    //process serial input
    if(Serial.available()){
      inChar=Serial.read();

      //we update the pointer to point to the appropriate value b/g/h handle ball,goal1,goal2
      if (inChar == 'b'){
        xpos = &bx; ypos = &by;
        inStr="";
      }
      else if (inChar == 'g'){
        xpos = &g1x; ypos = &g1y;
        inStr="";
      }
      else if (inChar == 'h'){
        xpos = &g2x; ypos = &g2y;
        inStr="";
      }
      //x/y means that the x/y-coordinate is finished
      else if (inChar=='x'){

        //special actions that we only want to happen when dealing with x-value of ball
        if (*xpos==bx) {
          if (inStr.toInt()<60 and inStr.toInt()>40){
            goForward();
            dribbler.drive(60);
          }
          else if (bx<60 and inStr.toInt()>=60){
            kickStartLeft();
            dribbler.stop();
          }
          else if (bx>40 and inStr.toInt()<=40){
            kickStartRight();
            dribbler.stop();
          }

          //show where we think the ball is
          if (inStr.toInt()>=50){
            digitalWrite(LED_BUILTIN,HIGH);
          }
          else if (inStr.toInt()<50){
            digitalWrite(LED_BUILTIN,LOW);
          }
        }

        *xpos=inStr.toInt();
        inStr="";
      }
      else if (inChar=='y'){
        //if we're close to the ball, charge it
        if (*ypos==by and inStr.toInt()>75){
          goForward();
          dribbler.drive(60);
        }
        
        *ypos=inStr.toInt();
        inStr="";
      }
      //if we're lost, turn right
      else if (inChar=='l'){
        kickStartRight();
        dribbler.stop();
      }
      //u is a command to stop the bot
      else if (inChar=='u'){
        stopAll();
        dribbler.stop();
      }
      else {
        inStr+=inChar;
      }
    }
  }
  //if we aren't going, we should probably stop
  else {
    stopAll();
    dribbler.stop()
  }
}

void goForward(){
  motorFrontLeft.drive(100);
  motorFrontRight.drive(-100);
  motorBackLeft.drive(100);
  motorBackRight.drive(-100);
}
void turnRight(){
  motorFrontLeft.drive(10);
  motorFrontRight.drive(10);
  motorBackLeft.drive(10);
  motorBackRight.drive(10);
}
void kickStartRight(){
  //start motors at a high power and drop to lower
  motorFrontLeft.drive(100);
  motorFrontRight.drive(100);
  motorBackLeft.drive(100);
  motorBackRight.drive(100);

  delay(60);
  turnRight();
}
void turnLeft(){
  motorFrontLeft.drive(-10);
  motorFrontRight.drive(-10);
  motorBackLeft.drive(-10);
  motorBackRight.drive(-10);  
}
void kickStartLeft(){
  //start motors at a high power and drop to lower
  motorFrontLeft.drive(-100);
  motorFrontRight.drive(-100);
  motorBackLeft.drive(-100);
  motorBackRight.drive(-100);

  delay(60);
  turnLeft();
}
void stopAll(){
  motorFrontLeft.stop();
  motorFrontRight.stop();
  motorBackLeft.stop();
  motorBackRight.stop();
}

