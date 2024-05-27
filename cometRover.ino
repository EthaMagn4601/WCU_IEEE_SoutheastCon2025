#define A_ENCA 16 // Yellow Wire for Motor A
#define A_ENCB 10 // White Wire for Motor A
#define A_PWM 5 // PWM Control for Motor A
#define INA1 14 // Direction control for IN1 of Motor A
#define INA2 15 // Direction control for IN2 of Motor A

#define B_ENCA 19 // Yellow Wire for Motor B
#define B_ENCB 18 // White Wire for Motor B
#define B_PWM 6 // PWM Control for Motor B
#define INB1 20 // Direction Control for IN1 of Motor B
#define INB2 21 // Direction Control for IN2 of Motor B

int A_pos = 0;
int B_pos = 0;

void setup() {
  Serial.begin(9600);
  pinMode(A_ENCA, INPUT);
  pinMode(A_ENCB, INPUT);
  pinMode(B_ENCA, INPUT);
  pinMode(B_ENCB, INPUT);
  
  // digitalInterrupt triggers on RISING edge of Motor A ENCA
  attachInterrupt(digitalPinToInterrupt(A_ENCA), A_readEncoder, RISING);
  attachInterrupt(digitalPinToInterrupt(B_ENCA), B_readEncoder, RISING);
}

void loop() {
  //(int A_dir, int A_PWMVal)
  A_setMotor(1, 10);
  delay(200);
  Serial.println(A_pos);
  A_setMotor(-1, 25);
  delay(200);
  Serial.println(A_pos);
  A_setMotor(0, 25);
  delay(200);
  Serial.println(A_pos);
}
