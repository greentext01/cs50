# Autowater
#### Video Demo:  <https://youtu.be/8zI_DlwATzI>
#### Description:

Hello, I’m Olivier Audet-Yang, I come from Ottawa, Canada, and I’d like to present a project that I made for CS50. It’s called “Autowater”.

It’s an IOT device for watering your garden when it’s dry. It also uploads moisture data to a website and phone app that I made with Ionic. You can also control the threshold for watering using the app or website.

For the hardware, I use an ESP32 that I programmed with c++. An ESP32 is a device sort of like an Ardruino, but it can connect to wifi. I also use this moisture sensor [shows moisture sensor] to measure the soil’s moisture. Finally, there is a solenoid, which is a electronically controlled valve.

When the device first boots, it connects to wifi. Then, it goes into a loop to check every 6 seconds if the moisture detected by a moisture sensor is bigger than the current threshold. If it is, it lets water out. If it isn’t, it doesn’t. 

But every 5 minutes, it sends the moisture data to a web server, which responds with a threshold. The ESP32 then updates the threshold.

Inside `Autowater-srv/` is the backend that I made with Flask. It receives the moisture data from the ESP32 and stores it in a database. It also stores the threshold and sends it to the device.

Inside `autowater/` is the user interface for the web server. It doesn’t use Flask’s templates, because I wanted it to also be an app for your phone.

It uses Ionic and Angular to do it. Ionic makes the website look like a phone app, and generates both an Android and IOS app.

Inside `autowater/src/app/tab1/` is a chart shows the moisture and threshold over time. It is generated using chart.js.

Inside `autowater/src/app/tab1/` is a form to modify the threshold. It sends a request to an endpoint on the Flask server, and gives you a message to let you know the threshold was updated.
