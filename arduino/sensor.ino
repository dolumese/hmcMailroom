#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

#define MIN2MS     60*1000  // 1000 ms -> 1 sec; 60 sec -> 1 min
#define POSTRATE   5*MIN2MS // POST to server every timestep
#define BUFFERSIZE 50       // JSON Buffer size
#define IN_PIN 5
#define OUT_PIN 12

int sensorStatus, httpCode;
char JSONmessageBuffer[BUFFERSIZE];

void setup() {
  Serial.begin(115200);                        // Serial connection
  
  pinMode(IN_PIN, INPUT_PULLUP);
  pinMode(OUT_PIN, OUTPUT);

  digitalWrite(OUT_PIN, HIGH);
  
  WiFi.begin("CINE", "");   // WiFi connection
 
  while (WiFi.status() != WL_CONNECTED) {      // Wait for the WiFI connection completion
    delay(500);
    Serial.println("Waiting for connection...");
  }
}
 
void loop() {
  if (WiFi.status() == WL_CONNECTED) {       // Connected to WIFI?
    sensorStatus = digitalRead(IN_PIN);
    
    StaticJsonBuffer<BUFFERSIZE> JSONbuffer; // Declaring static JSON buffer
    JsonObject& JSONencoder = JSONbuffer.createObject(); 
 
    JSONencoder["doorStatus"] = sensorStatus; // read from the sensor; is the door open or closed?
 
    JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
    
    Serial.println(JSONmessageBuffer); 
 
    HTTPClient http;    // Declare object of class HTTPClient
 
    http.begin("http://hmcmailroom.pythonanywhere.com/"); // Specify request destination
    http.addHeader("Content-Type", "application/json");   // Specify content-type header
 
    httpCode = http.POST(JSONmessageBuffer); // Send the request    
    String payload = http.getString();                                        //Get the response payload
 
    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload
 
    http.end();  // Close connection
  } else {
    Serial.println("Error in WiFi connection");
  }
 
  delay(POSTRATE); 
}

