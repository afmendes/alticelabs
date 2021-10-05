#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>
//FirebaseESP8266.h must be included before ESP8266WiFi.h
#include "FirebaseESP8266.h"  // Install Firebase ESP8266 library
#include <ESP8266WiFi.h>


// Firebase Settings
//#define FIREBASE_HOST "projetopi-a6e3d.firebaseio.com"
#define FIREBASE_HOST "https://alticelabs-92294-default-rtdb.europe-west1.firebasedatabase.app/"
#define FIREBASE_AUTH "KjuNiK5QmFqedv6b2DiV3lLAoK7RfdRwPkStGsJo"

//Define FirebaseESP8266 data object
FirebaseData firebaseData;
FirebaseData light_OnOff;
FirebaseData light_Bright;


//network credentials - must be updated
#define WIFI_SSID "SSID"           
#define WIFI_PASSWORD "PASSWORD"


//strings that will contain the directory of various variables in the cloud
String location_light_OnOff;
String location_light_Bright;


const uint16_t kIrLed = 4;  // ESP8266 GPIO pin - IREmmiter. Recommended: 4 (D2).
IRsend irsend(kIrLed);  // Set the GPIO to be used to sending the message.

//flags
int flag_wifi_on = 0;
int flag_connect_wifi = 1;

;

/*
*setup
*/
void setup() {
  
  irsend.begin();
#if ESP8266
  Serial.begin(115200, SERIAL_8N1, SERIAL_TX_ONLY);
#else  // ESP8266
  Serial.begin(115200, SERIAL_8N1);
#endif  // ESP8266

  location_light_OnOff = "ESP/Light/OnOff";
  location_light_Bright = "ESP/Light/Bright";

}

/*
*this method will run on a loop
*
*/
void loop() {
 
  
  if(flag_connect_wifi == 1){  
    //trying to connect to wifi


    //debug prints
    Serial.println("Attemping:");
   
    // connect to wifi.
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("connecting");
    
    //try to establish the connection during 30 seconds
    //if connection fails, it prints "connection failed" on the console
    unsigned long startedWaiting2 = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - startedWaiting2 <= 30000) {
      Serial.print(".");
      delay(500);
    }

     //not connected to wifi
    if(WiFi.status() != WL_CONNECTED){
      flag_wifi_on = 0;
      flag_connect_wifi = 1;
      Serial.println();
      Serial.print("\nConnection failed: ");
      
    //connected to wifi
    }else{
      flag_wifi_on = 1;
      flag_connect_wifi = 0;
      Serial.print("\nConnected: ");
      Serial.println(WiFi.localIP());
  
      //firebase begin
      Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
      Firebase.reconnectWiFi(true);
      
      
    }
    
  }else{


    
    //updates flags based on wifi conection and database remote option
    if(WiFi.status() != WL_CONNECTED){
      if(flag_wifi_on) Serial.println("WIFI CONNECTION LOST");
      flag_wifi_on = 0;
      flag_connect_wifi = 1;
    }
    
    
    //Serial.println(Firebase.getString(light_OnOff, location_light_OnOff));
    //connected to wifi and firebase started 
    if (Firebase.getString(light_OnOff, location_light_OnOff)){
      Serial.println(light_OnOff.stringData());
      if (light_OnOff.stringData() == "ON") {
        //turn ON command
        irsend.sendNEC(0xF7C03F);
        
        
      }
      else if (light_OnOff.stringData() == "OFF"){
        //turn OFF command
        irsend.sendNEC(0xF740BF);
        
      }
    }


    if (Firebase.getInt(light_Bright, location_light_Bright)){
      Serial.println(light_Bright.intData());
      if (light_Bright.intData() == 1) {
        ////more brightness
        irsend.sendNEC(0xF700FF);

        if (Firebase.setIntAsync(firebaseData, location_light_Bright, 0))
        {
          //must be 0
          Serial.println(light_Bright.intData());
        }
        
      }
      else if (light_Bright.intData() == -1){
        //less brightness
        irsend.sendNEC(0xF7807F);

        if (Firebase.setIntAsync(firebaseData, location_light_Bright, 0))
        {
          //must be 0
          Serial.println(light_Bright.intData());
        }
      }
    }
  }
  
  delay(1000);
  Serial.println("*");
}
