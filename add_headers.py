import os
import pandas as pd

folder_path = './testdata'
headers = ['Time', 'sensor1', 'sensor2', 'sensor3', 'sensor4', 'sensor5', 'sensor6', 'sensor7', 'sensor8', 'humidity', 'temperature']

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path, header=None) 
        
        # Check for headers
        if df.iloc[0].tolist() == headers:
            print(f'Headers already exist in {filename}')
            # df = df[df.apply(lambda row: row.tolist() != headers, axis=1)]
            df.drop(index=1)
            df.to_csv(file_path, index=False)

            continue
        
        # Add headers to the DataFrame
        df.columns = headers

        # Remove any additional headers if they exist

        # Save the DataFrame back to the CSV file
        df.to_csv(file_path, index=False)

        print(f'Headers added to {filename}')

print('All files processed.')