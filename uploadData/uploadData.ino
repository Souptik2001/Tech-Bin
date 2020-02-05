#include "HX711.h"
#include <WiFi.h>
#include <HTTPClient.h>
 
const char* ssid = "mynet";
const char* password =  "helloworld";

String uname = "souptikdatta"; /*The username of the dustbin owner*/

/*There will be two ESP32 one will have two attachments with Bio and Non_bio dustbins another will be connected to only one attachment to E_waste dustbin*/
String attachments = "double"; /*double if connected to two dustbins single if connected to one dustbin*/

//HX711 scale;
//float calibration_factor = -6075; // this calibration factor is adjusted according to my load cell
//float units;
 
void setup() {
 
  Serial.begin(115200);
  delay(4000);   //Delay needed before calling the WiFi.begin
 
  WiFi.begin(ssid, password); 
 
  while (WiFi.status() != WL_CONNECTED) { //Check for the connection
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
 
}
 
void loop() {
 
 if(WiFi.status()== WL_CONNECTED){   //Check WiFi connection status
 
   HTTPClient http;   
   String data;
   if (attachments == "double"){
      String bio = "70";
      String non_bio = "80";
//      String data = "{\"bio\":\"" + bio + "\",\"non_bio\":\"" + non_bio + "\",\"e_waste\":\"" + e_waste + "\"}";
      String data = "{\"bio\":\"" + bio + "\",\"non_bio\":\"" + non_bio + "\",\"attach\":\"" + attachments + "\"}";
   }
   else{
      String e_waste = "90";
      String data = "{\"e_waste\":\"" + e_waste + "\",\"attach\":\"" + attachments + "\"}";
   }
   String common_address = "https://tech-bin.souptikdatta.repl.co/upload/";
   String path = "https://tech-bin.souptikdatta.repl.co/upload/" + uname;
   http.begin(path);  //Specify destination for HTTP request
   http.addHeader("Content-Type", "application/json");             //Specify content-type header
 
   int httpResponseCode = http.POST(data);   //Send the actual POST request
 
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
