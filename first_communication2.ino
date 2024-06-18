 const int trigPin = 4;
 void setup() {
  Serial.begin(74880);
  while(!Serial){}
  pinMode(trigPin, INPUT);
}

void loop() {
  digitalWrite(trigPin,HIGH);
  if (digitalRead(trigPin) == LOW){
    Serial.println("Pin 4 is grounded");
  }
  delay(10);
}
