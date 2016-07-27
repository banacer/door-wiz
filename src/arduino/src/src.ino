#define maxlen 50

int pingPin[3] = {3, 5, 7}; //{T,R,L}
int max_timeout[3] = {12000, 6500, 6500}; //{T,R,L}
int data[3];
short inc = 0;
short Pin = 0;
short count = 0;
short idx = 0;
short sleep_left = 0;
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
  sleep_left = (max_timeout[inc] - duration)/1000;
  //data[inc] = sleep_left;
  if(inc == 1)
    sleep_left += 3;
  if(sleep_left >= 0)
    delay(sleep_left);
  inc++;
  if( inc == 3) {
    Serial.print(data[0]);
    Serial.print(",");
    Serial.print(data[1]);
    Serial.print(",");
    Serial.println(data[2]);
  }
  inc = inc % 3;

}

