import os
import pandas as pd

folder_path = './OIL_DATA_MULTIPLE_ADULTERANTS'
destination = './OIL_DATA_MULTIPLE_ADULTERANTS/output'

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        print(file_path,filename)
        df = pd.read_csv(file_path)
        if 'Time' in df.columns:
            output_path = os.path.join(destination, filename)
            print(f"Processing {file_path}...")
            df = df.drop(columns=['Time'])
            df.to_csv(output_path, index=False)
            print("done")