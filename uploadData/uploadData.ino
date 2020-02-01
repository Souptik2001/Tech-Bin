#include <bits/stdc++.h> 
using namespace std; 
#include <iostream>
#include <WiFi.h>
#include "HX711.h"
#include <HTTPClient.h>
#include <ArduinoJson.h>
const char uname[] = "souptikdatta";

const int LOADCELL_DOUT_PIN=4;
const int LOADCELL_SCK_PIN=5;

HX711 scale;
const char* ssid = "mynet";
const char* password =  "helloworld";

float calibration_factor = 2230; // this calibration factor must be adjusted according to your load cell
float units;

void setup() {

  Serial.begin(115200);
  delay(4000);   //Delay needed before calling the WiFi.begin

  WiFi.begin(ssid, password); 

  while (WiFi.status() != WL_CONNECTED) { //Check for the connection
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

  Serial.println("Connected to the WiFi network");

  // load cell initialization
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  
  Serial.println("HX711 calibration sketch");
  Serial.println("Remove all weight from scale");
  Serial.println("After readings begin, place known weight on scale");
  Serial.println("Press + or a to increase calibration factor");
  Serial.println("Press - or z to decrease calibration factor");

  scale.set_scale();
  scale.tare();  // Reset the scale to 0

  long zero_factor = scale.read_average(); // Get a baseline reading
  Serial.print("Zero factor: "); // This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  Serial.println(zero_factor);

}

void loop() {

  
 if(WiFi.status()== WL_CONNECTED){   //Check WiFi connection status

   HTTPClient http;

   Serial.println("—————");
   StaticJsonDocument<300> doc;
   char json[] = "{\"bio\":\"50\",\"non_bio\":\"40\",\"e_waste\":\"60\"}";
   deserializeJson(doc,json);   
//    root["bio"] = "30";
//    root["non_bio"] = "40";
//    root["e_waste"] = "50";

//   char common_address[] = "127.0.0.0.5000/upload/";
//   char address[] = "127.0.0.0.5000/upload/" + uname 
//   strcat(common_address,uname);   
//   http.begin(common_address);  //Specify destination for HTTP request
     http.begin("https://geeky-page--souptikdatta.repl.co/");  //Specify destination for HTTP request
   http.addHeader("Content-Type", "application/json");             //Specify content-type header

//   String data;
//   serializeJson(doc, data);
    

//   int httpResponseCode = http.POST(data);   //Send the actual POST request
    int httpResponseCode = http.GET(); 


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

  delay(5000);  //Send a request every 5 seconds
  scale.set_scale(calibration_factor);

  Serial.print("Reading: ");
  units = scale.get_units(), 10;

  float grams = units*17.5;

  if (grams < 0) {
    grams = 0.00;
  }
  
  Serial.print(grams);
  Serial.print(" grams"); 
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor);
  Serial.println();

  // if calibration input is received
  if(Serial.available())
  {
    char temp = Serial.read();
    if(temp == '+' || temp == 'a')
      calibration_factor += 1;
    else if(temp == '-' || temp == 'z')
      calibration_factor -= 1;
  }

}
