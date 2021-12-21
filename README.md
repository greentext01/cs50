# CS50 Final Project - Autowater
#### Video Demo:  <https://youtu.be/8zI_DlwATzI>

Technologies used:

* Angular
* Flask
* SQLite3
* C++
* ESP32 Http library
* ESP32 WIFI library
* Arduino IDE
* pbkdf2_sha256
* Python
* JavaScript
* Capacitor
* Chart.js
* Ionic
* Android Studio
* HTML
* CSS
* Other small JavaScript libraries

## How does it work?

The user first buys a device, and puts it in their garden. The device senses if the soil is dry and waters it if it is. The user can also visit a website where he can see how wet the soil was overtime, and can control the threshold for watering using a form, on the website. The user can also download a phone app to do the same as the website.

#### Hardware

For the hardware, Autowater uses an ESP32 that I programmed with c++. An ESP32 is a device sort of like an Arduino, but it can connect to WIFI. I also use a moisture sensor to measure the soil’s moisture. Finally, there is a solenoid, which is a electronically controlled valve, used to control the flow of water.

When the device first boots, it connects to WIFI. Then, it goes into a loop to check every 6 seconds if the moisture detected by a moisture sensor is bigger than the current threshold. If it is, it lets water out. If it isn’t, it doesn’t. 

But every 5 minutes, it sends the moisture data to a web server, which responds with a threshold. The ESP32 then updates the threshold.

#### API

Autowater has an API that the hardware accesses to upload moisture data, and to receive the threshold. It is also accessed by the frontend to read moisture data and update the threshold.

* When you send a `POST` request to `/` with the moisture amount and the right password, it responds with the threshold.

* When you send a `GET` request to `/api/moisture` it responds with the last 200 moisture values.

* When you send a `POST` request to `/api/threshold` with a threshold and the right password, it updates the threshold.

#### Frontend

Autowater has a frontend made with Angular and Ionic. If you go to the home page, it displays a graph made with Chart.js showing the moisture overtime. You can zoom and scroll on it. The frontend gets the data using the API.

If you click on "Tab 2", it shows a form that you can use to change the threshold. It makes a request to the API to change it. When you submit it, it shows a toast notification to let you know that the threshold has changed.

#### Potential improvements

Like every other app, this app can be improved. Here are some ways I could have made it better:

* Better hardware: For now, the hardware consists of a Tupperware with a breadboard, the ESP32, The solenoid valve, and a bunch of confusing jumper wires. I could use a PCB, and a better box.

* An account system: For now, it only has one password, and no username.
