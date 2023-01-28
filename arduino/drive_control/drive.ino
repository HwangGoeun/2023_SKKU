#include <Car_Library.h>
#include <ros.h>
#include <std_msgs/String.h>

///////////////////////////////////////////
int motorA1_1 = 1;
int motorA1_2 = 2;

int motorB1_1 = 3;
int motorB1_2 = 4;

int motorB2_1 = 5;
int motorB2_2 = 6;
///////////////////////////////////////////

ros::NodeHandle nh;
String motor_run;

void move_go(){
  
  motor_backward(motorB1_1,motorB1_2,100);
  motor_forward(motorB2_1,motorB2_2,100);

  motor_backward(motorA1_1,motorA1_2,255);
  delay(300);
  motor_forward(motorA1_1,motorA1_2,255);
  delay(300);
}

void move_left(){
  
  motor_backward(motorB1_1,motorB1_2,100);
  motor_forward(motorB2_1,motorB2_2,100);
  
  motor_backward(motorA1_1,motorA1_2,255);
  delay(300);
  motor_forward(motorA1_1,motorA1_2,255);
  delay(300);

}

void move_right(){
  
  motor_forward(motorB1_1,motorB1_2,100);
  motor_forward(motorB2_1,motorB2_2,100);

  motor_backward(motorA1_1,motorA1_2,255);
  delay(300);
  motor_forward(motorA1_1,motorA1_2,255);
  delay(300);
}

void move_stop(){
  
  motor_hold(motorB1_1,motorB1_2);
  motor_hold(motorB2_1,motorB2_2);

  motor_hold(motorA1_1,motorA1_2);
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
