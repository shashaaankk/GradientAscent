import pandas as pd
import numpy as np
import gpxpy
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
import os
import glob
import sys
from scipy.stats import zscore
import matplotlib.pyplot as plt
import zipfile
import requests

# Define file and directory paths
data_dir = "data"
zip_path = os.path.join(data_dir, "gpx-hike-tracks.zip")
download_url = "https://www.kaggle.com/api/v1/datasets/download/roccoli/gpx-hike-tracks"

# Ensure the data directory exists
os.makedirs(data_dir, exist_ok=True)

# Check if the zip file already exists
if not os.path.exists(zip_path):
    print("Downloading dataset...")
    response = requests.get(download_url, allow_redirects=True)
    if response.status_code == 200:
        with open(zip_path, "wb") as f:
            f.write(response.content)
        print("Download complete.")
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")
else:
    print("Zip file already exists. Skipping download.")

# Unzip the file
print("Extracting files...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(data_dir)
print("Extraction complete.")

csv_path = os.path.join("data", "gpx-tracks-from-hikr.org.csv")

# Read and inspect
df = pd.read_csv(csv_path)

df = df.dropna()
df = df[df["start_time"]!=df["end_time"]]
df = df[df["length_3d"]!=0]
df = df[df["moving_time"]!=0]
# Convert time columns to datetime
df["start_time"] = pd.to_datetime(df["start_time"], format="%Y-%m-%d %H:%M:%S" , errors='coerce')
df["end_time"] = pd.to_datetime(df["end_time"], format="%Y-%m-%d %H:%M:%S" ,errors='coerce')

# Compute total duration in seconds
df["duration"] =  df["moving_time"]

# Compute break time: duration - moving_time
df["break_time"] = (df["end_time"] - df["start_time"]).dt.total_seconds() - df["moving_time"]

df["speed"] = df["length_3d"] / df["duration"] 
# Select relevant features
df = df[df["break_time"]>=0]
df = df[df["break_time"]<1.5*df["duration"]]
df = df[df["speed"]<5]
selected = df[["duration","length_3d", "min_elevation", "max_elevation", "uphill", "downhill", "break_time"]]  
X = selected
y = df['difficulty'].str[1].astype(int)

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

model = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),   # ← new name
    n_estimators=50,
    random_state=42
)
#model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Wrap back into a DataFrame, preserving column names
# X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

output_path = os.path.join("data", "output.csv")
# X_scaled_df.to_csv(output_path, index=False)
X.to_csv(output_path, index=False)