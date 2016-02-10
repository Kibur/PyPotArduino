#define TESTLED 13
#define ANALOG 5
#define GO 103
#define STOP 115

int data = STOP;

void setup() {
  pinMode(TESTLED, OUTPUT);
  Serial.begin(9600);
}

void sendData(int data) {
  Serial.print("p:->");
  Serial.print(data);
  Serial.println("<");
}

void readPotentiometer(int val) {
  digitalWrite(TESTLED, HIGH);
  delay(500);
  digitalWrite(TESTLED, LOW);
  delay(500);

  sendData(val);
}

void readSerial(int val) {
  Serial.print("--Arduino received: ");
  Serial.println(val);

  if (val == 121)
    digitalWrite(TESTLED, HIGH);
  else
    digitalWrite(TESTLED, LOW);
}

void loop() {
  if (data == GO)
    readPotentiometer(analogRead(ANALOG));
  else if (data == STOP)
    digitalWrite(TESTLED, LOW);

  if (Serial.available() > 0) {
    data = Serial.read();
    readSerial(data);
  }
}
