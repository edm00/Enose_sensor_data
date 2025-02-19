import os
import pandas as pd
import numpy as np

# Folder containing the CSV files
input_folder_path = 'C:/Users/info/OneDrive/Desktop/enose/code/Enose_device_code_3.0/new_device_data'


# Folder to save the modified CSV files
output_folder_path = 'C:/Users/info/OneDrive/Desktop/enose/code/Enose_device_code_3.0/modified/'

# Create the output folder if it doesn't exist
os.makedirs(output_folder_path, exist_ok=True)

# Columns to fix
columns_to_fix = ['temperature', 'humidity']

# List to store data from all files
all_data = []

# Read all CSV files and store data
for filename in os.listdir(input_folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder_path, filename)
        df = pd.read_csv(file_path)
        all_data.append(df)

# Concatenate all data
combined_data = pd.concat(all_data)

# Calculate mean for the specified columns
mean_values = combined_data[columns_to_fix].mean(skipna=True, numeric_only=True)

# Fill NA values in each file and save to the output folder
for filename in os.listdir(input_folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder_path, filename)
        df = pd.read_csv(file_path)
        # print(df.dtypes)
        df[columns_to_fix[0]] = df[columns_to_fix[0]].fillna(0)
        df[columns_to_fix] = df[columns_to_fix].replace(0, mean_values)
        output_file_path = os.path.join(output_folder_path, filename)
        df.to_csv(output_file_path, index=False)

print("NA values filled and files saved successfully to the modified folder.")