#define maxlen 50
#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
int pingPin[3] = {3, 5, 7}; //{T,R,L}
int max_timeout[3] = {6000, 3250, 3250}; //{T,R,L}
int timeout;
int data[3];
short inc = 0;
short Pin = 0;
short count = 0;
short idx = 0;
short sleep_left = 0;
int i = 0;
int temp_count = 0;
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
  duration = pulseIn(Pin, HIGH,timeout);
  if(duration == 0)
    duration = timeout;
}

void setup()
{
  Serial.begin(9600);
  dht.begin();
}

void loop()
{
  temp_count++;
  Pin = pingPin[inc];
  timeout = max_timeout[inc];
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
    Serial.print(data[2]);
    if(temp_count == 18000) { //This is for sending temperature every 5 minutes given avg sampling rate
	temp_count = 0;
    	float f = dht.readTemperature(true);
	Serial.print(",");
    	if(isnan(f))
	    Serial.println("Error in DHT");
    	else
            Serial.println(f);
    }
    else
	Serial.println("");

  }
  inc = inc % 3;

}