#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <FastLED.h>
#include <ArduinoJson.h>

#include "config.h"

//General Setup 
//Apparently this is important. 5V Step down is 10A. We'll round down to 8A
#define MILLI_AMPS 8000

//Defaults
#define DEFAULTS_SET false
int BRIGHTNESS;
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
    Serial.println("Connecting to WiFi..");
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

  //Get default values
  if (!DEFAULTS_SET) {
    //DO SOME GET STUFF AND WRITE TO EEPROM
  } else {
    //READ FROM EEPROM
  }

  //Initialize LED Strips
  FastLED.addLeds<LED_TYPE, D5, COLOR_ORDER>(leds, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, D6, COLOR_ORDER>(leds, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, D7, COLOR_ORDER>(leds, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, D8, COLOR_ORDER>(leds, NUM_LEDS_PER_STRIP);
  //FastLED.setDither(false); //you may see the dithered pixel output as flickering, and you may want to turn it off if the effect is distracting. It's not magic; it's up to you what looks good in your projects.﻿
  FastLED.setCorrection(Typical8mmPixel);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, MILLI_AMPS);

  //Setup LEDs on power-on
  FastLED.setBrightness(BRIGHTNESS);
  if (ANIMATION) {
    //Set animation if animation is enabled
    //setAnimation();
  } else {
  }
  FastLED.show();
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  //Svar tilbage med POST (hele JSON-objekt som kom fra MQTT)
  String payloadString;
  for (int i = 0; i < length; i++) {
    payloadString += (char)payload[i];
  }
  Serial.println(payloadString);
  mqttToJson(payloadString);
}

//Manipulate JSON String and get values
void mqttToJson (String receivedJSON) {
  String json = receivedJSON;
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& jsonResult = jsonBuffer.parseObject(json);

  //Get animation stirng
  String animationJSON = jsonResult["Animation"];

  //Get brightness and convert from 0-100 to 0-255 to fit FastLED
  float brightnessJSON = jsonResult["Brightness"]; //(X*255)/100 0-100 -> 0-255
  brightnessJSON = (brightnessJSON * 255)/100;

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
  FastLED.setBrightness(255);
  
  if (ANIMATION != NULL) {
    for (int i = 0; i < NUM_LEDS_PER_STRIP; i++) {
      leds[i].setRGB(COLOR[0], COLOR[1], COLOR[2]); FastLED.delay(33); leds[i] = CRGB::Black;
    }
  } else {
    Serial.println("Animation. Do things!");
  }
  FastLED.show();
}

void loop() {
  client.loop();
}

