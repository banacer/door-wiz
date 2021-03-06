#define maxlen 50

int pingPin[3] = {
  3, 5, 7}; //{T,R,L}
short inc = 0, Pin;
short count = 0, idx = 0;

unsigned long data[3];
int i = 0;

int statusLed = 11;
int errorLed = 12;

short temp = 0, lowest, tempInch = 0, refVal = 11;
float inches, cm;
unsigned long duration = 0;

void getDuration()
{
  pinMode(Pin, OUTPUT);
  digitalWrite(Pin, LOW);
  delayMicroseconds(2);
  digitalWrite(Pin, HIGH);
  delayMicroseconds(5);
  digitalWrite(Pin, LOW);

  pinMode(Pin, INPUT);
  duration = pulseIn(Pin, HIGH,15000);

}

void setup()
{
  Serial.begin(9600);	
}

void loop()
{
  Pin = pingPin[inc];
  getDuration();	
  data[inc] = duration;
  inc++;
  //delay(3);
  if( inc == 3) {
    Serial.print(data[0]);
    Serial.print(",");
    Serial.print(data[1]);
    Serial.print(",");
    Serial.println(data[2]);

  }
  inc = inc % 3;

}

