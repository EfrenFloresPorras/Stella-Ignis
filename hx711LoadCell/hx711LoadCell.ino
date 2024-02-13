#include <HX711_ADC.h> // need to install 
#include <Wire.h>

HX711_ADC LoadCell(6, 7); // parameters: dt pin 6, sck pin 7;
unsigned long t = 0;

void setup() 
{
  Serial.begin(57600); 
  LoadCell.begin(); // start connection to HX711
  LoadCell.start(2000); // load cells gets 2000ms of time to stabilize
  LoadCell.setCalFactor(1000); // calibration factor for load cell => dependent on your individual setup
}

void loop() {
  float i = LoadCell.getData(); // get output value
  static boolean newDataReady = 0;
  const int serialPrintInterval = 0; //increase value to slow down serial print activity

  // check for new data/start next conversion:
  if (LoadCell.update()) newDataReady = true;

  // get smoothed value from the dataset:
  if (newDataReady) {
    if (millis() > t + serialPrintInterval) {
      float i = LoadCell.getData();
      Serial.print("Weight[g]: ");
      Serial.println(i);
      newDataReady = 0;
      t = millis();
    }
  }
}