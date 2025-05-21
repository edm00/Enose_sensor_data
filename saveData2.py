import serial
import csv
import time
from datetime import datetime

ser = serial.Serial('COM8', 9600)  # Adjust to your port and baud rate
context = {'Sample': 'mustard_oil', 'Iteration':2, 'ver': 'A'}
readings = 1
num_of_sensors = 8  # Number of sensors
temp_n_humidity = 0

with open(f'./MEMS_DATA_P6.0_A/{context["Sample"]}-{context["Iteration"]}{context["ver"]}.csv', 'x', newline='') as csvfile:
    fieldnames = ['Time', 'sensor1', 'sensor2', 'sensor3', 'sensor4', 'sensor5',
                  'sensor6', 'sensor7', 'sensor8', 'humidity', 'temperature']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


    delay = True
    i = 10
    while True:
        try:
            if delay:
                time.sleep(2)  # Wait for sensors to stabilize
                delay = False

            line = ser.readline().decode('utf-8').rstrip()
            data = line.split(',')  # Expecting 10 values (8 sensors + humidity + temp)
            dt = datetime.now()
            timestamp = dt.timestamp()
            # print(len(data))
            if len(data) == 1:
                print(line)

            if len(data) == num_of_sensors + temp_n_humidity:  # Ensure complete data
                if i % 5 == 0:
                    print(data)  # Print every 5th line for debugging
                i += 1

                writer.writerow({
                    'Time': int(timestamp),
                    'sensor1': data[0],
                    'sensor2': data[1],
                    'sensor3': data[2],
                    'sensor4': data[3],
                    'sensor5': data[4],
                    'sensor6': data[5],
                    'sensor7': data[6],
                    'sensor8': data[7],
                    # 'humidity': data[8],
                    # 'temperature': data[9]
                })

                # terminate the program after N readings
            # print(len(data) == 1 ,data[0])
            # N = data[0].split(" ")[1]
            # print("N = ",N)
            N = readings - 1
            if len(data) == 1 and  data[0] == f'Finished {N}':
                    print("Terminating...")
                    break
        except KeyboardInterrupt:
            print("Terminating...")
            break
        except (ValueError, IndexError) as e:
            print(f"Error processing line: {line} - {e}")
            continue

ser.close()
