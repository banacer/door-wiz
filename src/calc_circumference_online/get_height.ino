#define pingPin 5


short temp = 0, duration = 0, lowest, tempInch = 0, refVal = 11;
short inches, cm;

short time2cm(short duration)
{
	short cm;
	cm = duration/29/2;
	return cm;
}

short time2inch(short duration)
{
	short inch;
	inch = duration/74/2;
	return inch;
}


short getDuration(void)
{
	pinMode(pingPin, OUTPUT);
	digitalWrite(pingPin, LOW);
	delayMicroseconds(2);
	digitalWrite(pingPin, HIGH);
	delayMicroseconds(5);
	digitalWrite(pingPin, LOW);

	pinMode(pingPin, INPUT);
	duration = pulseIn(pingPin, HIGH);
	return duration;

}

short getLowest(void)
{
	short temp1 = 100,ref = 11;
	duration = getDuration();
	temp1 = inches;
//	Serial.print("temp1 = ");
//	Serial.println(temp1);
	inches = time2inch(duration);
//	Serial.print("inches  = ");
//	Serial.println(inches);
	while(inches != ref)
	{
		duration = getDuration();
		temp1 = inches;
//		Serial.print("temp1 = ");
//		Serial.println(temp1);
		inches = time2inch(duration);
//		Serial.print("inches  = ");
//		Serial.println(inches);

		if(inches < temp1)
		{
			lowest = inches;
		}
		else
		{
			lowest = lowest;
		}
		Serial.print("lowest  = ");
		Serial.println(lowest);
//		Serial.println();
//		Serial.println();
                delay(150);

	}

//	Serial.print("lowest  = ");
//        Serial.println(lowest);
	delay(2000);
	return lowest;

}

void setup()
{
	Serial.begin(9600);
}

void loop()
{  
	getLowest();
	// Serial.println("In Main");
//	Serial.print("lowest = ");
//	Serial.println(lowest);
//	Serial.println();
	delay(20);

}
