#include <XBee.h>
#include <math.h>
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
struct point {
	double x;
	double y;
};

TxStatusResponse txStatus = TxStatusResponse();

int statusLed = 11;
int errorLed = 12;

short temp = 0, lowest, tempInch = 0, refVal = 11;
float inches, cm;
short duration = 0;
float w_max = 145.0;
short started = 0; 
short done = 0;
double ul = 0;
double ur = 0;
double first = 0;
double last = 0;
struct point l_prev,r_prev;
double left_sum = 0, right_sum = 0;
double length = 0;
double circumference = 0;
short s_circum = 0;
float time2cm(float duration)
{
	cm = duration/29.0/2.0;
	return cm;
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
double euclideanDistance(struct point a, struct point b)
{
    return sqrt(pow(a.x-b.x,2) + pow(a.y-b.y,2));
}
	
void setup()
{
	Serial.begin(9600);	
	xbee.setSerial(Serial);
        l_prev.x = 0;
        l_prev.y = 0;
        r_prev.x = 0;
        r_prev.y = 0;
	
}

void loop()
{  
	Pin = pingPin[inc];
	getDuration();
	cm = time2cm(duration);
        
        if(inc == 3)
        {
      	  length+= 0.08*13;			
			if(cm >= w_max) //IGNORE THIS READING
			{

				//length = 0;
				//w_max = cm;
			}
			else if(cm <= 0.7*w_max)
			{				
				ul = cm;
				
			}
			else if (0.9*w_max <= cm && cm <= 0.99*w_max) // THIS MAY MEAN THAT NO ONE IS PASSING BY 
			{
				//INITIALIZE ALL VARIABLES AND FINISH UP THE CALCULATION IF NOT YET DONE
				if(first != 0 && last != 0)
				{
					if(right_sum > 0)
					{
						circumference = left_sum + right_sum + first +last + 10;
                                                //SENDING THE CIRCUMFERENCE
                                                 s_circum = (short) circumference;
                                                 payload[0] = 6;
                                                 payload[1] = s_circum >> 8 & 0xff;
                                                 payload[2] = s_circum & 0xff;
                                                 xbee.send(tx);
						//cout << "circumference: " << circumference << ", left: " << left_sum << ", right: " << right_sum << ", first: " << first << ", last: " << last << endl;
						//cout << "circumference: "<< circumference << endl;
					}
					//printf("circumference = %f\n",circumference);
					//INITIALIZING VARIABLES
					length = 0;
					left_sum = 0;
					right_sum = 0;

					r_prev.x = 0;
					r_prev.y = 0;
					l_prev.x = 0;
					l_prev.y = 0;

					first  = 0;
					last = 0;
				}
			}
        }
	if(inc == 4)
        {      	  
      	                length+= 0.08; 			
			if(cm <= 0.7*w_max && ul > 0)
			{	
				
				ur = cm;
				double width = w_max - ur - ul;
				
				if(width > 0)
				{
					
					if(first == 0 || (length - r_prev.y) > 10)// the second condition is when the first is very noted long go
					{
						first  = width;
						//cout << "first: " <<first << ", length: " << length << endl;						
					}
					else
					  last = width;
					//now compute the lengths
					struct point r_current,l_current;
					
					if(r_prev.y == 0 && l_prev.y == 0) // THIS IS BECAUSE IT THE FIRST POINT SO JUST SAVE IT IN THE PREVIOUS TO BE USE IN THE NEXT ROUND
					{
						r_prev.x = width/2;
						r_prev.y = length;
						l_prev.x = width/2;
						l_prev.y = length;
					}
					else
					{
						r_current.x = width/2;
						r_current.y = length;
						l_current.x = width/2;
						l_current.y = length;
						if((l_current.y - l_prev.y) < 5.0)
						{
							//cout << "width: " << width << ", ur: " << ur <<", ul: " << ul << ", length: "<< length <<endl;
							left_sum += euclideanDistance(l_current,l_prev);
							right_sum += euclideanDistance(r_current,r_prev);
						}
						else
						{
							left_sum = 0;
							right_sum = 0;

						}


						r_prev.x = r_current.x;
						r_prev.y = r_current.y;
						l_prev.x = l_current.x;
						l_prev.y = l_current.y;
					}
				}
			}
             
      	  
        }
	
	inc++;
	inc = inc % 3;
}
