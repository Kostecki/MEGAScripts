##### Configurations are defined in the `config.h` file. An example is provided with the repo.

```
//Environment
const int env = 0; //0 = development, 1 = production

//Online firmware update
const int FW_VERSION = 1; //Increment when updating
const char* fwUrlBase = ""; //

//WIFI
#if env == 0
    const char* ssid = "";
    const char* password = "";
#else
    const char* ssid = "";
    const char* password = "";
#endif

//MQTT
const char* mqtt_server = "";
const char* mqtt_username = "";
const char* mqtt_password = "";
const int mqtt_port = ;
const char* mqtt_in = "";

//OTA
#define SENSORNAME "" //change this to whatever you want to call your device
#define OTApassword "" //the password you will need to enter to upload remotely via the ArduinoIDE
int OTAport = ;
```
