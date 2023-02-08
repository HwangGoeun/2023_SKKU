#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include <WProgram.h>
#endif
#include <stdlib.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/String.h>
#include <Car_Library.h>

ros::NodeHandle nh;
geometry_msgs::Twist msg;

///////////////

int left_motor_speed = 80; 
int right_motor_speed = 80;
int steering = 90;
int left_steering = 255;
int right_steering = 255;

/////////////

float move1;
float move2;


///////////////////////////////////////////////
const int motorA1_1 = 3;
const int motorA1_2 = 4;

const int motorB1_1 = 5;
const int motorB1_2 = 6;

const int motorB2_1 = 8;
const int motorB2_2 = 9;

////////////////////////////////////////////////

void front()  //press key i (I)
{
  motor_backward(motorB1_1,motorB1_2,left_motor_speed);
  delay(100);
  motor_forward(motorB2_1,motorB2_2, right_motor_speed);
  delay(100);
 
  motor_backward(motorA1_1,motorA1_2,steering);
  delay(100);
}

void back()   //press key , (, 쉼표 맞음)
{
  motor_backward(motorB2_1,motorB2_2,left_motor_speed);
  delay(100);
  motor_forward(motorB1_1,motorB1_2,right_motor_speed);
  delay(100); 
}

void left()   //press key j (J)
{ 
  motor_backward(motorB1_1,motorB1_2,left_motor_speed);
  delay(100);
  motor_forward(motorB2_1,motorB2_2, right_motor_speed);
  delay(100);
  motor_forward(motorA1_1,motorA1_2,left_steering);
  delay(100);  
}

void right()    //press key l (L)
{ 
  motor_forward(motorB1_1,motorB1_2,left_motor_speed);
  delay(100);
  motor_forward(motorB2_1,motorB2_2,right_motor_speed);
  delay(100);
  motor_backward(motorA1_1,motorA1_2,right_steering);
  delay(100);
}

void die()    //press key k or s (K or S)
{
  motor_hold(motorB1_1,motorB1_2);
  delay(100);
  motor_hold(motorB2_1,motorB2_2);
  delay(100);
  motor_hold(motorA1_1,motorA1_2);
  delay(100);
}

void callback(const geometry_msgs::Twist& cmd_vel)
{
  move1 = cmd_vel.linear.x;
  move2 = cmd_vel.angular.z;
  
  if (move1 > 0 && move2 == 0)
  {
    front();
  }
  
  else if (move1 > 0 && move2 > 0 )
  {
    left();
  }
  
  else if (move1 > 0 && move2 < 0 )
  {
    right();
  }
  
  else if (move1 < 0)
  {
    back();
  }
  
  else
  {
    die();
  }
  
}

ros::Subscriber <geometry_msgs::Twist> sub("/cmd_vel", callback);

void setup() {
  
  Serial.begin(57600);
  
  pinMode(motorA1_1, OUTPUT);
  pinMode(motorA1_2, OUTPUT);
  
  pinMode(motorB1_1, OUTPUT);
  pinMode(motorB1_2, OUTPUT);
  
  pinMode(motorB2_1, OUTPUT);
  pinMode(motorB2_2, OUTPUT);

nh.initNode();
nh.subscribe(sub);

}

void loop() {
nh.spinOnce();
delay(1);
}
