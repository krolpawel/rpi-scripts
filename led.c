#include <stdio.h>
#include <wiringPi.h>

int main (void)
{
	printf("Pierwszy projekt\n");
	if(wiringPiSetup () == -1)
	return 1;
	pinMode(0,OUTPUT);
while(1)
{
	digitalWrite(0,1); //dioda on
	delay(100);
	digitalWrite(0,0); //dioda off
	delay(100);
}
	return 0;
}

