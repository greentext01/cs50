#include <HTTPClient.h>
#include <WiFi.h>

const char *ssid = "NETGEAR_5GEXT";
const char *password = "AAE666A6";
int threshold = 2000;
int passed = 0;

void setup() {
    // put your setup code here, to run once:
    Serial.begin(9600);
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print('.');
        delay(1000);
    }

    Serial.println(WiFi.localIP());

    pinMode(2, OUTPUT);
}

void loop() {
    passed++;

    if (analogRead(34) > threshold) {
        digitalWrite(2, LOW);
    } else {
        digitalWrite(2, HIGH);
    }

    if (passed == 50) {
        HTTPClient http;

        http.begin("http://autowater.ddns.net:5000/");
        http.addHeader("Content-Type", "application/x-www-form-urlencoded");
        if (http.POST("moisture=" + String(analogRead(34)) +
                      "&password=olivier") == 200) {
            threshold = http.getString().toInt();
        }

        passed = 0;
    }

    delay(6 * 1000);
    // put your main code here, to run repeatedly:
}