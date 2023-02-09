#include <Car_Library.h>

//////////////////////////////////

int left_motor_speed = 70; 
int right_motor_speed = 70;
int steering = 80;
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

void move_go(){
  
  motor_backward(motorB1_1,motorB1_2,left_motor_speed);
  delay(100);
  motor_forward(motorB2_1,motorB2_2, right_motor_speed);
  delay(100);
 
  motor_hold(motorA1_1,motorA1_2);
  delay(100);

}

void move_left(){
  
  motor_backward(motorB1_1,motorB1_2,left_motor_speed);
  delay(100);
  motor_forward(motorB2_1,motorB2_2, right_motor_speed);
  delay(100);

  motor_hold(motorA1_1,motorA1_2);
  delay(100);
}

void move_right(){
  
  motor_backward(motorB1_1,motorB1_2,left_motor_speed);
  delay(100);
  motor_forward(motorB2_1,motorB2_2,right_motor_speed);
  delay(100);
  
  motor_hold(motorA1_1,motorA1_2);
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

//
void move_back_steering(){
  
  motor_forward(motorB1_1,motorB1_2,left_motor_speed);
  delay(100);
  motor_backward(motorB2_1,motorB2_2,right_motor_speed);
  delay(100);

  motor_hold(motorA1_1,motorA1_2);
  delay(100);
  
}

void move_back(){
  
  motor_forward(motorB1_1,motorB1_2,left_motor_speed);
  delay(100);
  motor_backward(motorB2_1,motorB2_2,right_motor_speed);
  delay(100);
  

    motor_hold(motorA1_1,motorA1_2);
  delay(100);
  
}

void setup() {

  pinMode(motorA1_1, OUTPUT);
  pinMode(motorA1_2, OUTPUT);
  
  pinMode(motorB1_1, OUTPUT);
  pinMode(motorB1_2, OUTPUT);
  
  pinMode(motorB2_1, OUTPUT);
  pinMode(motorB2_2, OUTPUT);

  ///////////////////////////////////////
  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  
  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);

  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);

  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  
  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  
  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  
  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  
  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);

  
  //
  motor_forward(motorA1_1,motorA1_2,255);
  delay(1000);
  move_go();
  delay(3000);

  motor_backward(motorA1_1,motorA1_2,255);
  delay(1000);
  move_back();
  delay(11000);
/////////////////////////////////////
  move_stop();
  delay(4000);
//////////////////////////////////////
  motor_backward(motorA1_1,motorA1_2,255);
  delay(3000);
  move_go();
  delay(15000);
  //
  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);


  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);

  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);

  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);

  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);

  motor_forward(motorA1_1,motorA1_2,150);
  delay(1000);
  move_go();
  delay(1000);
  motor_backward(motorA1_1,motorA1_2,150);
  delay(1000);

  
}

void loop() {

}
