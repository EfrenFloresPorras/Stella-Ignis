/* Arduino code for a precision scale with a 1Kg load cell, HX711 ADC and mode selector 
 * Schematic: https://electronoobs.com/eng_arduino_tut115_sch1.php
 * Code: https://electronoobs.com/eng_arduino_tut115_code1.php
 * Video: https://youtu.be/LRd3W_p8PJ4 */


#include <Q2HX711.h>              //Downlaod from here: https://electronoobs.com/eng_arduino_hx711.php
//LCD config
#include <Wire.h> 


//Pins 
const byte hx711_data_pin = 3;    //Data pin from HX711
const byte hx711_clock_pin = 2;   //Clock pin from HX711
int tara_button = 8;              //Tara button
int mode_button = 11;             //Mode change button
Q2HX711 hx711(hx711_data_pin, hx711_clock_pin); // prep hx711

//Variables
/////////Change here with your calibrated mass////////////
float y1 = 256.1; // calibrated mass to be added
//////////////////////////////////////////////////////////

long x1 = 0L;
long x0 = 0L;
float avg_size = 10.0; // amount of averages for each mass measurement
float tara = 0;
bool tara_pushed = false;
bool mode_pushed = false;
int mode = 0;
float oz_conversion = 0.035274;
//////////////////////////////////////////////////////////



void setup() {
  Serial.begin(9600);                 // prepare serial port
  PCICR |= (1 << PCIE0);              //enable PCMSK0 scan                                                 
  PCMSK0 |= (1 << PCINT0);            //Set pin D8 trigger an interrupt on state change.
  PCMSK0 |= (1 << PCINT3);            //Set pin D10 trigger an interrupt on state change.   
  pinMode(tara_button, INPUT_PULLUP);
  pinMode(mode_button, INPUT_PULLUP);

  
  delay(1000);                        // allow load cell and hx711 to settle

  
  // tare procedure
  for (int ii=0;ii<int(avg_size);ii++){
    delay(10);
    x0+=hx711.read();
  }
  x0/=long(avg_size);
  Serial.println("Add Calibrated Mass");
  // calibration procedure (mass should be added equal to y1)
  int ii = 1;
  while(true){
    if (hx711.read()<x0+10000)
    {
      //do nothing...
    } 
    else 
    {
      ii++;
      delay(2000);
      for (int jj=0;jj<int(avg_size);jj++){
        x1+=hx711.read();
      }
      x1/=long(avg_size);
      break;
    }
  }
  Serial.println("Calibration Complete");
}

void loop() {
  // averaging reading
  long reading = 0;
  for (int jj=0;jj<int(avg_size);jj++)
  {
    reading+=hx711.read();
  }
  reading/=long(avg_size);

  
  
  // calculating mass based on calibration and linear fit
  float ratio_1 = (float) (reading-x0);
  float ratio_2 = (float) (x1-x0);
  float ratio = ratio_1/ratio_2;
  float mass = y1*ratio;

  if(tara_pushed)
  {
    tara = mass;
    tara_pushed = false;
    Serial.print("TARA");
    Serial.print(".");
    delay(300);
    Serial.print(".");
    delay(300);
    Serial.println(".");
    delay(300);   
  }
  if(mode_pushed)
  {
    mode = mode + 1;
    mode_pushed = false;
    if(mode > 2)
    {
      mode = 0;
    }
  }
  
  if(mode == 0)
  {
    Serial.print(mass - tara);
    Serial.println(" g");
  }
  else if(mode == 1)
  {
    Serial.print(mass - tara);
    Serial.println(" ml");
  }
  else
  {
    Serial.print((mass - tara)*oz_conversion);
    Serial.println(" oz");
  }
  
}//End of void loop


//interruption to detect buttons
ISR(PCINT0_vect)
{
  if (!(PINB & B00000001))
  {
    tara_pushed = true;           //Tara button was pushed
  }
  
  if (!(PINB & B00001000))
  {
    mode_pushed = true;           //Mode button was pushed
  }
}

 
  
