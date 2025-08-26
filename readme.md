## ESP32 Remote Peripheral Control with MQTT
### Overview

![alt text](docu/overview.png "Overview")
### Detailed description

![alt text](docu/Client-Waveshare-ESP32C6.png "Title")

### Install
Flash the latest micropython version to the ESP32-C6 Zero board.   
Copy adc.py, boot.py, gpio.py and main.py into the root of the ESP32-C6.  
Note: Only ESP32-C6 is tested. Maybe it is running on other ESP32 but not guaranteed.  
#### Limitations
After using pin as gpio output it cannot be reused as pwm pin  


