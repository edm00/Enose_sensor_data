import os
import pandas as pd

folder_path = '.'  # Current directory

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        if 'time' in df.columns:
            df = df.drop(columns=['Time'])
            df.to_csv(file_path, index=False)