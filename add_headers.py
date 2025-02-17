import os
import pandas as pd

# Define the folder path where your CSV files are located
folder_path = './new_device_data'

# Define the headers you want to add
headers = ['Time', 'sensor1', 'sensor2', 'sensor3', 'sensor4', 'sensor5',
           'sensor6', 'sensor7', 'sensor8', 'humidity', 'temperature']

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path, header=None)  # Assuming no headers are present

        # Add headers to the DataFrame
        df.columns = headers

        # Save the DataFrame back to the CSV file
        df.to_csv(file_path, index=False)

        print(f'Headers added to {filename}')

print('All files processed.')