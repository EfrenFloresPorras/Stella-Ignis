/*

Propiedad de STELLA IGNIS
By Efren Flores y Emiliano Arias

Resumen de código: El código propiamente es una edición preliminar (v.1.0.0). 
Esta hecho para que unicamente se reciba en la terminal los valores de fuerza aplicada y se pueda utilizar con el siguiente código "csv_pruebas.py"
*/


#include <HX711_ADC.h> // need to install from Arduino Library
#include <Wire.h>

HX711_ADC LoadCell(6, 7); // parameters: dt pin 6, sck pin 7;
unsigned long t = 0;

void setup() 
{
  Serial.begin(57600); // Serial Monitor frequency used
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
      Serial.println(i);
      newDataReady = 0;
      t = millis();
    }
  }
}
