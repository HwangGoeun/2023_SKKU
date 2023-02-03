#include <Car_Library.h>
#include <ros.h>
#include <std_msgs/String.h>

//////////////////////////////////

int left_motor_speed = 80; 
int right_motor_speed = 80;
int steering = 90;
int left_steering = 255;
int right_steering = 255;

///////////////////////////////////////////
int motorA1_1 = 3;
int motorA1_2 = 4;

int motorB1_1 = 5;
int motorB1_2 = 6;

int motorB2_1 = 8;
int motorB2_2 = 9;
///////////////////////////////////////////

ros::NodeHandle nh;
String motor_run;

void move_go(){
  
  motor_backward(motorB1_1,motorB1_2,left_motor_speed);
  delay(100);
  motor_forward(motorB2_1,motorB2_2, right_motor_speed);
  delay(100);
 
  motor_backward(motorA1_1,motorA1_2,steering);
  delay(100);
  motor_hold(motorA1_1,motorA1_2);
  delay(100);  

}

void move_left(){
  
  motor_backward(motorB1_1,motorB1_2,left_motor_speed);
  delay(100);
  motor_forward(motorB2_1,motorB2_2, right_motor_speed);
  delay(100);
  motor_forward(motorA1_1,motorA1_2,left_steering);
  delay(100);  
}

void move_right(){
  
  motor_forward(motorB1_1,motorB1_2,left_motor_speed);
  delay(100);
  motor_forward(motorB2_1,motorB2_2,right_motor_speed);
  delay(100);
  
  motor_backward(motorA1_1,motorA1_2,right_steering);
  delay(100);
  
}

void move_stop(){
  
  motor_hold(motorB1_1,motorB1_2);
  delay(100);
  motor_hold(motorB2_1,motorB2_2);
  delay(100);

  motor_hold(motorA1_1,motorA1_2);
  delay(100);
}

void direction_cb(const std_msgs::String& msg) {

 
  motor_run=msg.data;

  

  if (motor_run == "LEFT"){
    move_left();
  }

  else if (motor_run == "RIGHT"){
    move_right();
  }

  else if (motor_run == "STOP"){
    move_stop();
  }
  
  else if (motor_run == "GO"){
      move_go();
  }
  
}

ros::Subscriber <std_msgs::String> sub("direction", &direction_cb);

void setup(){
  
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

void loop(){
  nh.spinOnce();
  delay(1);
  
}
