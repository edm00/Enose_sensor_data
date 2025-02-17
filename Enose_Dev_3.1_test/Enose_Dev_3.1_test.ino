// #include <Arduino.h>
#include <DHT.h>

#define DHTPIN 12 // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11 // DHT 11 sensor
#define DHTTYPE2 DHT22 // DHT 22 sensor

DHT dht(DHTPIN, DHTTYPE2);

const int fanPin = 3; // Pin for the fan
const int numSensors = 8; // Number of analog sensors
const int sensorPins[numSensors] = { A0, A1, A2, A3, A4, A5, A6, A7}; // Analog sensor pins

const unsigned long stableDelay = 5000; // 5 seconds for sensors to stabilize
const unsigned long readingDuration = 40000; // 40 seconds for reading
const unsigned long fanRunTime = 35000; // 35 seconds for fan run time
 int counter = 0; 
bool temp = true;
// const int relayPin = 8;  // Pin connected to IN1 of the relay module


void setup() {
    Serial.begin(9600);
    dht.begin();

    //  pinMode(relayPin, OUTPUT);  // Set the relay pin as an output
    //  digitalWrite(relayPin, LOW);  // Ensure the relay is off initially

    pinMode(fanPin, OUTPUT);
    digitalWrite(fanPin, LOW); // Start with fan off

    // Allow time for serial monitor to open
    delay(1000);
    Serial.println("Fan starting...");
    // Run fan to clear chamber
    digitalWrite(fanPin, HIGH);
    delay(fanRunTime);
    digitalWrite(fanPin, LOW);
    delay(1000); // Small delay before starting readings
}

void loop() {
    // Stabilize the sensors
    delay(stableDelay);

    // digitalWrite(relayPin, HIGH);  // Relay is active LOW, so HIGH turns it ON
    // delay(10000);  // Keep the pump ON for 5 seconds

  // Turn the air pump OFF
    // digitalWrite(relayPin, LOW);  // Turn the relay OFF
    // delay(5000);  // Keep the pump OFF for 5 seconds
 
    // Prepare to read sensor data
    unsigned long startTime = millis();
    float sensorValues[numSensors];
    float tempValue;
    float humidity = dht.readHumidity();
    float temperatureC = dht.readTemperature();
    // Read sensors for 30 seconds
    while (millis() - startTime < readingDuration) {
        for (int i = 0; i < numSensors; i++) {
            sensorValues[i] = analogRead(sensorPins[i]);
        }
        // tempValue = analogRead(tempSensorPin);

        // Send data to Serial for Python logging
        // Serial.print("Sensors: ");
        for (int i = 0; i < numSensors; i++) {
            Serial.print(sensorValues[i]);
            if (i < numSensors - 1) {
                Serial.print(", ");
            }
        }
        // Serial.print(" | Temp: ");
        if(temp)
        {
            Serial.print(", ");
        Serial.print(humidity);
        Serial.print(", ");
        Serial.println(temperatureC);
        };
            // Serial.println("");
       
        
        // Serial.println("");

        // Delay for next reading (can adjust based on desired sampling rate)
        delay(1000); // Sample every 1000ms
    }
  Serial.println("Readings taken for " + String(readingDuration/1000)+"s");
  Serial.println("Finished "+String(counter++));
    
    // Run fan again to clear chamber
    digitalWrite(fanPin, HIGH);
    delay(fanRunTime);
    digitalWrite(fanPin, LOW);
    delay(1000); // Small delay before next cycle
}

