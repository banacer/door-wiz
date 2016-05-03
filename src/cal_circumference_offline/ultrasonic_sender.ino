#include <XBee.h>
#include "Timer.h"
Timer t;
int pingPin[3] = {3, 5, 7};
short inc = 0, Pin;
XBee xbee = XBee();
// allocate three bytes for to hold a 10-bit analog reading
uint8_t payload[3];

// with Series 1 you can use either 16-bit or 64-bit addressing

// 16-bit addressing: Enter address of remote XBee, typically the coordinator
Tx16Request tx = Tx16Request(0x2210, payload, sizeof(payload));


TxStatusResponse txStatus = TxStatusResponse();

int statusLed = 11;
int errorLed = 12;

short temp = 0, lowest, tempInch = 0, refVal = 11;
float inches, cm;
short duration = 0;


float time2cm(float duration)
{
	cm = duration/29.0/2.0;
	return cm;
}

float time2inch(short duration)
{
	float inch;
	inch = duration/74.0/2.0;
	return inch;
}


void getDuration()
{
	pinMode(Pin, OUTPUT);
	digitalWrite(Pin, LOW);
	delayMicroseconds(2);
	digitalWrite(Pin, HIGH);
	delayMicroseconds(5);
	digitalWrite(Pin, LOW);

	pinMode(Pin, INPUT);
	duration = pulseIn(Pin, HIGH);
	//return duration;
}

	
void setup()
{
	Serial.begin(9600);	
	xbee.setSerial(Serial);
}

void loop()
{  
	Pin = pingPin[inc];
	getDuration();	
	payload[0] = inc + 3;
        payload[1] = duration >> 8 & 0xff;
        payload[2] = duration & 0xff; 
	xbee.send(tx);
	inc++;
	inc = inc % 3;

}
