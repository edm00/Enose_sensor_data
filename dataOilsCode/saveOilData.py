import serial
import csv
import time
import os
from datetime import datetime

# Configuration
ser = serial.Serial('COM8', 9600)
readings = 40                      # Readings per sample
num_of_sensors = 8
temp_n_humidity = 0               # Set to 2 if including humidity/temp
output_dir = './OIL_DATA_MULTIPLE_ADULTERANTS'

# Define base oil and its adulterants
base_oil = 'Mustard'
# adulterants = ['Canola', 'SoyaBean', 'Sunflower']
# adulterants = ['Canola']
adulterants = ['Sunflower']
# adulterants = ['SoyaBean']   #---->Change
# Define adulteration levels (from 0% to 100% in 10% increments)
adulteration_levels = [i for i in range(0, 110, 10)]

sample_number = 8  #increment +1   #---->Change
# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Start data collection
for adulterant in adulterants:

        adulterant_pct = adulteration_levels[sample_number]
        base_oil_pct = 100 - adulterant_pct

        # File naming format: Mustard_with_Canola_90-10.csv
        filename = f'{base_oil}_{adulterant}_{base_oil_pct}-{adulterant_pct}.csv'
        filepath = os.path.join(output_dir, filename)

        print(f"\n>>> Starting sample: {filename} <<<")

        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ['Time'] + [f'sensor{i+1}' for i in range(num_of_sensors)]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            delay = True
            i = 0
            while i < readings:
                try:
                    if delay:
                        print("Waiting for sensors to stabilize...")
                        time.sleep(30)
                        delay = False

                    line = ser.readline().decode('utf-8').rstrip()
                    data = line.split(',')
                    timestamp = int(datetime.now().timestamp())
                    time.sleep(1)
                    # Skip debug/info lines from Arduino
                    if len(data) == 1:
                        print("Message:", line)
                        continue

                    if len(data) == num_of_sensors + temp_n_humidity:
                        writer.writerow({
                            'Time': timestamp,
                            **{f'sensor{j+1}': data[j] for j in range(num_of_sensors)}
                        })

                        if i % 5 == 0:
                            print(f"Reading {i+1}/{readings}: {data}")
                        i += 1

                except KeyboardInterrupt:
                    print("Manual interruption. Exiting...")
                    ser.close()
                    exit()
                except (ValueError, IndexError) as e:
                    print(f"Error processing line: {line} - {e}")
                    continue

print(f"\n>>> Data collection completed {adulterants[0]} level{adulteration_levels[sample_number]} <<<")
ser.close()
