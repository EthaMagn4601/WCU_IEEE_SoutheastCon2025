void setup() {
  Serial.begin(115200);
  while (!Serial){}
  pinMode(4, INPUT);
}

void loop() {
  digitalWrite(4, HIGH);
  if (digitalRead(4) == LOW){
    Serial.println("Pin 4 is grounded");
  }
  delay(10);
}
