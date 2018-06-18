#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <FastLED.h>
#include <ArduinoJson.h>

#include "config.h"

//General Setup 
//Apparently this is important. Our 5V step down is 10A. We'll round down to 8A ¯\_(ツ)_/¯
#define MILLI_AMPS 8000

//Defaults
float BRIGHTNESS;
int* COLOR;
String ANIMATION;

//LED Setup
#define LED_TYPE WS2813
#define NUM_LEDS_PER_STRIP 38
#define COLOR_ORDER GRB
#define FRAMES_PER_SECOND 240

//Network Setup
#define HOSTNAME "MEGABoominatorLEDS"
const char* ssid = "MEGABoominator";

//MQTT Setup
const char* mqttServer = "puma.rmq.cloudamqp.com";
const int mqttPort = 1883; //8883 for TLS
const char* mqttUser = "rynflejx:rynflejx";
const char* mqttTopic = "boominator";

CRGB leds[NUM_LEDS_PER_STRIP];

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  delay(3000);
  
  //Setup EEPROM
  EEPROM.begin(512);

  //Enable serial output.. i guess?
  Serial.begin(115200);
  delay(100);

  //Setup and Connect to WiFi
  WiFi.setSleepMode(WIFI_NONE_SLEEP);
  WiFi.hostname(HOSTNAME);
  WiFi.begin(ssid, wifiPassword);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }

  //Setup and Connect to MQTT Broker
  client.setServer(mqttServer, mqttPort);
  client.setCallback(mqttCallback);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {
      Serial.println("Connected to Topic: " + String(mqttTopic));  
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
  client.subscribe(mqttTopic);

  //Initialize LED Strips
  FastLED.addLeds<LED_TYPE, D5, COLOR_ORDER>(leds, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, D6, COLOR_ORDER>(leds, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, D7, COLOR_ORDER>(leds, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, D8, COLOR_ORDER>(leds, NUM_LEDS_PER_STRIP);
  //FastLED.setDither(false); //you may see the dithered pixel output as flickering, and you may want to turn it off if the effect is distracting. It's not magic; it's up to you what looks good in your projects.﻿
  FastLED.setCorrection(Typical8mmPixel);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, MILLI_AMPS);
}

void loop() {
  client.loop();

  FastLED.show();
}

//Handle MQTT response
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  //Svar tilbage med POST (hele JSON-objekt som kom fra MQTT)
  String payloadString;
  for (int i = 0; i < length; i++) {
    payloadString += (char)payload[i];
  }
  mqttToJson(payloadString);
}

//Manipulate JSON String and get values
void mqttToJson (String receivedJSON) {
  Serial.println(receivedJSON);
  String json = receivedJSON;
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& jsonResult = jsonBuffer.parseObject(json);

  //Get animation stirng
  String animationJSON = jsonResult["Animation"];

  //Get brightness and convert from 0-100 to 0-255 to fit FastLED
  float brightnessJSON = jsonResult["Brightness"];
  brightnessJSON = (brightnessJSON * 255);

  //Get individual R, G, B and A values
  int rJSON = jsonResult["Color"]["R"];
  int gJSON = jsonResult["Color"]["G"];
  int bJSON = jsonResult["Color"]["B"];
  int rgbJSON[] = {rJSON, gJSON, bJSON};

  //Set global strip-variables (and save to EEPROM)
  ANIMATION = animationJSON;
  BRIGHTNESS = brightnessJSON;
  COLOR = rgbJSON;

  updateStrip();
}

void updateStrip () {
  FastLED.setBrightness(BRIGHTNESS);
  
  if (ANIMATION != "") {
    Serial.println("Solid Color");
    fill_solid(leds, NUM_LEDS_PER_STRIP, CRGB(COLOR[0], COLOR[1], COLOR[2]));
  } else {
    Serial.println("Animation");
  }
}

void SingleColorTravelingDot() {
  Serial.println("SingleColorTravelingDot");
  int travelSpeed = 50; //Higher is slower
  for(int i = 0; i < NUM_LEDS_PER_STRIP; i++) { 
    leds[i].setRGB(COLOR[0], COLOR[1], COLOR[2]);
    FastLED.show();
    // clear this led for the next time around the loop
    leds[i] = CRGB::Black;
    delay(travelSpeed);
  }
}
