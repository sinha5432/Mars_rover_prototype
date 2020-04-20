// Code for the ATtiny85
#define I2C_SLAVE_ADDRESS 0x4 // Address of the slave
    
#include "avr/interrupt.h";
 
#include <TinyWireS.h>



#define encoderPinA 1
#define encoderPinB 4



int encoderPos = 0;
 
 
void setup()
{
    TinyWireS.begin(I2C_SLAVE_ADDRESS); // join i2c network

    //attachInterrupt(0, doEncoder, RISING);
    
    GIMSK |= (1<<PCIE);
    PCMSK |= (1<<PCINT1);
    //MCUCR |= (1<<ISC01)|(1<<ISC02);

  
    

    pinMode(encoderPinA, INPUT_PULLUP);
   // digitalWrite(encoderPinA, HIGH);       // turn on pull-up resistor
    pinMode(encoderPinB, INPUT);
   // digitalWrite(encoderPinB, HIGH);       // turn on pull-up resistor 

   sei();
}
 
void loop()
{
     TinyWireS_stop_check();
   //  TinyWireS.send(encoderPos); 
    //TinyWireS.send(-25);         
}


  

ISR(PCINT0_vect)
{
  
  
  if (digitalRead(encoderPinA) == digitalRead(encoderPinB))
  {
    encoderPos++;
    //Serial.println("plus");
    TinyWireS.send(encoderPos);
  }
  else
  {
    encoderPos--;
    //Serial.println("minus");
    TinyWireS.send(encoderPos);
  }

  

  
 
}




  
