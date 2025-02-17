import pandas as pd
import io
from google.colab import files
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from google.colab import drive

def train_and_save_model(alcohol_url, air_url, model_filename):
    """
    Trains a model to classify alcohol and air data and saves it.

    Args:
      alcohol_url: URL to the alcohol dataset on Google Drive.
      air_url: URL to the air dataset on Google Drive.
      model_filename: Path to save the trained model on Google Drive.
    """

    def read_drive_file(url):
        try:
            file_id = url.split('/d/')[1].split('/view')[0]
            download_url = f'https://drive.google.com/uc?id={file_id}'
            data = pd.read_csv(download_url)
            return data
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    alcohol_df = read_drive_file(alcohol_url)
    air_df = read_drive_file(air_url)

    if alcohol_df is not None and air_df is not None:
        # ... (rest of your model training code from the original script)
        alcohol_df['class'] = 1
        air_df['class'] = 0
        combined_df = pd.concat([alcohol_df, air_df], ignore_index=True)
        combined_df.dropna(inplace=True)

        X = combined_df.drop(['Time', 'class'], axis=1)
        y = combined_df['class']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy}")
        print(classification_report(y_test, y_pred))

        drive.mount('/content/drive')  # Mount Google Drive if not already mounted
        joblib.dump(model, model_filename)
        print(f"Model saved to {model_filename}")

def perform_eda(dataframe, title):
    """
    Performs exploratory data analysis on a dataframe.
    """
    print(f"\n{title} Data:")
    print(dataframe.info())
    print(dataframe.describe())

    sensor_columns = [col for col in dataframe.columns if col != 'Time']

    plt.figure(figsize=(15, 10))
    for sensor in sensor_columns:
        plt.plot(dataframe['Time'], dataframe[sensor], label=sensor)
    plt.xlabel("Time")
    plt.ylabel("Sensor Value")
    plt.title(f"{title} Sensor Readings")
    plt.legend()
    plt.show()


    for sensor in sensor_columns:
        plt.figure(figsize=(8, 6))
        plt.scatter(dataframe['Time'], dataframe[sensor], label=f'{title} Sensor {sensor}', alpha=0.7)
        plt.xlabel("Time")
        plt.ylabel(f"Sensor {sensor} Value")
        plt.title(f"{title} Sensor {sensor} Readings over Time")
        plt.legend()
        plt.grid(True)
        plt.show()
