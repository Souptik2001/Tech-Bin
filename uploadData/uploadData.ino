/*
Three HX711 sensorsors are connected
Pin 13-> 1st HX711 CLK
Pin 14-> 1st HX711 DOUT
Pin VIN-> 1st HX711 VCC
Pin GND-> 1st HX711 GND
Pin 39-> 2nd HX711 CLK
Pin 35-> 2nd HX711 DOUT
Pin VIN-> 2nd HX711 VCC
Pin GND-> 2nd HX711 GND
Pin 33-> 3rd HX711 CLK
Pin 26-> 3rd HX711 DOUT
Pin VIN-> 3rd HX711 VCC
Pin GND-> 3rd HX711 GND
 
*/

#include "HX711.h"
#include <WiFi.h>
#include <HTTPClient.h>
 
const char* ssid = "mynet";
const char* password =  "helloworld";

String uname = "souptikdatta"; /*The username of the dustbin owner*/

const int LOADCELL_DOUT_PIN_1 = 14;
const int LOADCELL_SCK_PIN_1 = 13;
const int LOADCELL_DOUT_PIN_2 = 35;
const int LOADCELL_SCK_PIN_2 = 39;
const int LOADCELL_DOUT_PIN_3 = 26;
const int LOADCELL_SCK_PIN_3 = 33;

HX711 scale1;
HX711 scale2;
HX711 scale3;
float calibration_factor_1 = -6075; // |
float calibration_factor_2 = -6075; // |----> These are not callibrated. These should be callibrated acording to your load cell. 
float calibration_factor_3 = -6075; // |
float units_1;
float units_2;
float units_3;
 
void setup() {
 
  Serial.begin(115200);
  scale1.begin(LOADCELL_DOUT_PIN_1,LOADCELL_SCK_PIN_1);
  scale2.begin(LOADCELL_DOUT_PIN_2,LOADCELL_SCK_PIN_2);
  scale3.begin(LOADCELL_DOUT_PIN_3,LOADCELL_SCK_PIN_3);

  scale1.set_scale();
  scale1.tare();  //It resets scale to zero
  scale2.set_scale();
  scale2.tare();
  scale3.set_scale();
  scale3.tare();

  long zero_factor_1 = scale1.read_average();
  long zero_factor_2 = scale2.read_average();
  long zero_factor_3 = scale3.read_average();
  Serial.print("Zero Factor 1 : ");
  Serial.println(zero_factor_1);
  Serial.print("Zero Factor 2 : ");
  Serial.println(zero_factor_2);
  Serial.print("Zero Factor 3 : ");
  Serial.println(zero_factor_3);
  
  delay(4000);   //Delay needed before calling the WiFi.begin
 
  WiFi.begin(ssid, password); 
 
  while (WiFi.status() != WL_CONNECTED) { //Check for the connection
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
 
}
 
void loop() {

  scale1.set_scale(calibration_factor_1);
  scale1.set_scale(calibration_factor_2);
  scale1.set_scale(calibration_factor_3);

  Serial.print("Reading 1 : ");
  units_1 = scale1.get_units(), 10;
  int kg_1 = (17.5*units_1)/1000;
  Serial.print("Reading 2 : ");
  units_2 = scale2.get_units(), 10;
  int kg_2 = (17.5*units_2)/1000;
  Serial.print("Reading 3 : ");
  units_3 = scale3.get_units(), 10;
  int kg_3 = (17.5*units_3)/1000;

  if(kg_1<0){
    kg_1 = 0;
  }
    if(kg_2<0){
    kg_2 = 0;
  }
  if(kg_3<0){
    kg_3 = 0;
  } 
 if(WiFi.status()== WL_CONNECTED){   //Check WiFi connection status

   HTTPClient http;   
   String bio = String(kg_1);
   String non_bio = String(kg_2);
   String e_waste = String(kg_3);
   String info = "{\"bio\":\"" + bio + "\",\"non_bio\":\"" + non_bio + "\",\"e_waste\":\"" + e_waste + "\"}";
   Serial.println(info);
   String common_address = "https://tech-bin.souptikdatta.repl.co/upload/";
   String path = "https://tech-bin.souptikdatta.repl.co/upload/" + uname;
   http.begin(path);  //Specify destination for HTTP request
   http.addHeader("Content-Type", "application/json");             //Specify content-type header
   Serial.print("This is sent : ");
   Serial.println(info);
   int httpResponseCode = http.POST(info);   //Send the actual POST request
 
   if(httpResponseCode>0){
 
    String response = http.getString();                       //Get the response to the request
 
    Serial.println(httpResponseCode);   //Print return code
    Serial.println(response);           //Print request answer
 
   }else{
 
    Serial.print("Error on sending POST: ");
    Serial.println(httpResponseCode);
 
   }
 
   http.end();  //Free resources
 
 }else{
 
    Serial.println("Error in WiFi connection");   
 
 }
 
  delay(10000);  //Send a request every 10 seconds
 
}
