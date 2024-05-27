// A_setMotor() exists to set the motor direction (A_dir), speed (A_PWMVal [value ranging from 0-255]), 
// and write to specific motor driver pins (A_PWM, INA1, INA2) of Motor A
void A_setMotor(int A_dir, int A_PWMVal){
  analogWrite(A_PWM, A_PWMVal);
  if (A_dir == 1){
    digitalWrite(INA1, HIGH);
    digitalWrite(INA2, LOW);
  } // END if{}
  else if (A_dir == -1){
    digitalWrite(INA1, LOW);
    digitalWrite(INA2, HIGH);
  } // END else if{}
  else{
    digitalWrite(INA1, LOW);
    digitalWrite(INA2, LOW);
  } // END else{}
} // END A_setMotor()

// readEncoder() exists to read the position of A_ENCB on a successful rising edge trigger input of A_ENCA 
// (A_ENCB is LOW when motion is CCW & HIGH when motion is CW)
void A_readEncoder(){
  int A_b = digitalRead(A_ENCB);
  if (A_b > 0){
    A_pos++;
  } // END if{}
  else{
    A_pos--;
  } // END else{}
} // END A_readEncoder()

// B_setMotor functions exactly the same as A_setMotor but gives a specific output to the driver pins for Motor B 
void B_setMotor(int B_dir, int B_PWMVal){
  analogWrite(B_PWM, B_PWMVal);
  if (B_dir == 1){
    digitalWrite(INB1, HIGH);
    digitalWrite(INB2, LOW);
  } // END if{}
  else if (B_dir == -1){
    digitalWrite(INB1, LOW);
    digitalWrite(INB2, HIGH);
  } // END else if{}
  else{
    digitalWrite(INB1, LOW);
    digitalWrite(INB2, LOW);
  } // END else{}
} // END B_setMotor()

void B_readEncoder(){
  int B_b = digitalRead(B_ENCB);
  if (B_b > 0){
    B_pos++;
  } // END if{}
  else{
    B_pos--;
  }// END else{}
} // END B_readEncoder()
