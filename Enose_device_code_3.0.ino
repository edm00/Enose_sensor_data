// #include <Arduino.h>

const int fanPin = 10; // Pin for the fan
const int numSensors = 8; // Number of analog sensors
const int sensorPins[numSensors] = {A0, A1, A2, A3, A4, A5, A6, A7}; // Analog sensor pins
// const int tempSensorPin = 12; // Pin for temperature sensor
const unsigned long stableDelay = 25000; // 25 seconds for sensors to stabilize
const unsigned long readingDuration = 30000; // 30 seconds for reading
const unsigned long fanRunTime = 30000; // 30 seconds for fan run time

void setup() {
    Serial.begin(9600);
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

    // Prepare to read sensor data
    unsigned long startTime = millis();
    float sensorValues[numSensors];
    float tempValue;

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
        Serial.print(", ");
        Serial.println(tempValue);

        // Delay for next reading (can adjust based on desired sampling rate)
        delay(1000); // Sample every 1000ms
    }

    // Run fan again to clear chamber
    digitalWrite(fanPin, HIGH);
    delay(fanRunTime);
    digitalWrite(fanPin, LOW);
    delay(1000); // Small delay before next cycle
}

