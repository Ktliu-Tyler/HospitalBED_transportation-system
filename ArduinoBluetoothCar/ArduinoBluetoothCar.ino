#include <SoftwareSerial.h>
#include <Wire.h>
#include "MotorController.h"


// Define Motor Move Direction
#define L298N1_FORWARD "back"
#define L298N1_BACK "forward"
#define L298N2_FORWARD "forward"
#define L298N2_BACK "back"
#define L298N3_FORWARD "forward"
#define L298N3_BACK "back"
#define L298N4_FORWARD "back"
#define L298N4_BACK "forward"

byte motor1[3] = {2, 4, 3};
byte motor2[3] = {6, 7, 5};
byte motor3[3] = {8, 9, 10};
byte motor4[3] = {12, 13, 11};


MotorController controller = MotorController(motor1, motor2, motor3, motor4);

SoftwareSerial CAR_BT(0, 1); //定義 PIN0 及 PIN1 分別為 RX 及 TX 腳位

char Car_status;
byte Speed_value = 200;

void setup() {

  Serial.begin(9600);
  CAR_BT.begin(9600); 

  controller.motor_direction_setter(1, L298N1_FORWARD, L298N1_BACK);
  controller.motor_direction_setter(2, L298N2_FORWARD, L298N2_BACK);
  controller.motor_direction_setter(3, L298N3_FORWARD, L298N3_BACK);
  controller.motor_direction_setter(4, L298N4_FORWARD, L298N4_BACK);
  controller.stopAll();
}

void loop()
{
  int inSize;
  char input;
  if( (inSize = (CAR_BT.available())) > 0) { //讀取藍牙訊息
      Serial.print("size = ");
      Serial.println(inSize);
      Serial.print("Input = ");
      Serial.println(input=(char)CAR_BT.read());
      
      if( input == 'F' ) {
        controller.moveForward(Speed_value);
        Serial.print("Forward");
      }
      
      else if( input == 'B' ) {
        controller.moveBack(Speed_value);
        Serial.print("Backward");
      }
    
      else if( input == 'l' ) {
        controller.rotate("left", Speed_value);
        Serial.print("Left");
      }
      
      else if( input == 'r' ) {
        controller.rotate("right", Speed_value);
        Serial.print("Right");
      }
    
      else if( input == 'L' ) {
        controller.moveParallel("left", Speed_value);
        Serial.print("L_Parallel");
      }

      else if( input == 'R' ) {
        controller.moveParallel("right", Speed_value);
        Serial.print("R_Parallel");
      }
      else if( input == 'A' ) {
        controller.moveDiagonal("left", Speed_value);
        Serial.print("L_Diagonal");
      }

      else if( input == 'C' ) {
        controller.moveDiagonal("right", Speed_value);
        Serial.print("R_Diagonal");
      }

      else if( input == 's' ) {
        controller.stopAll();
        Serial.print("Stop");
      }
      
  }    
}
