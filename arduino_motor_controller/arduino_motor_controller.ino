

//
////////////////////////////////////
/// 1: Header

#include <Servo.h>       // Import servo libraries
Servo esc_left;          // Create a servo object named esc_left
Servo esc_right;         // Create another servo object for the right esc

String inString = "";    // define a string to hold received serial characters
int inChar = 0;          // define a variable to hold the latest character from serial
int thruster_left;       // define a variable to hold the latest signal to the left thruster
int thruster_right;      // define a variable to hold the latest signal to the right thruster
int led_pin = 13;
int data_collection_bool; 
int save_as_first = true;
int save_as_second = false;// define a logical element that tracks if values are part of the second value in the string
int save_as_third = false;

////////////////////////////////////
/// 2: Setup

void setup() {
  Serial.begin(115200);    // Open a serial channel at a baudrate of 9600
  esc_left.attach(9, 1300, 1700);  // Assign a servo object to pin 9
  esc_right.attach(10, 1300, 1700); // Assign a servo to pin 10
  pinMode(led_pin, OUTPUT);
}

////////////////////////////////////
/// 3: Main loop

void loop() {
  /// 3.1 : Read serial data

  if (Serial.available()) {  // If serial data is available.
    inChar = Serial.read();  // Save the latest byte
    inString += char(inChar);// Join the latest character to a growing string of recent chracters
    
    //Serial.println(inChar);
    /// 3.2 When a comma is detected, save the current string as a number and assign it to one of the output variables
    if (inChar == ',') {
      if (save_as_first == true) { // If the most recent chracter is a comma, confirm that the current string is the first value.
        thruster_left = inString.toInt(); // Save the string as an integer in one of our two output variables
        thruster_left = map(thruster_left, 0, 100, 1700, 1300);
        inString = "";               // Reset the string
        save_as_second = true;      // Indicate that the next value detected is for the second thruster
        save_as_first = false;
        //Serial.println(thruster_left);
      }
    }
    
    /// 3.3 When a semicolon is detected, save the current string as a number and assign it to the other output variables
    if (inChar == ';') {     // If the latest chracter is the end-of-line character...
      if (save_as_second == true) {
        thruster_right = inString.toInt();// Assign the most recent number string to the second thruster
        thruster_right = map(thruster_right, 0, 100, 1700, 1300);
        inString = "";        // Reset the string
        save_as_second = false;// Indicate that the next value detected is for the first thruster
        save_as_third = true;
      }
    }  
      /// 3.4 Write out the new values to the servos and to serial
    if (inChar == '.') {
      if (save_as_third == true) {
        data_collection_bool = inString.toInt();
        inString = "";
        save_as_third = false;
        save_as_first = true;
      }
    }

    // Write the signal value to one of the servo objects
    esc_left.write(thruster_left);
    esc_right.write(thruster_right);  

    if (data_collection_bool == 1) {
      digitalWrite(led_pin, HIGH);
    }
    else {
      digitalWrite(led_pin, LOW);
    }

  }
 
}
