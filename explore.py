import json
import pandas as pd

with open('raw_data/fda_recalls_raw.json') as f:
    data = json.load(f)

df = pd.json_normalize(data['results'])

print(f"Shape: {df.shape}")
print(f"\nColumns:\n{df.columns.tolist()}")
print(f"\nNull counts per column:\n{df.isnull().sum().sort_values(ascending=False)}")
print(f"\nSample row:\n{df.iloc[0]}")
print(f"\nUnique classification values:\n{df['classification'].value_counts()}")
print(f"\nUnique status values:\n{df['status'].value_counts()}")
print(f"\nDate format sample (report_date):\n{df['report_date'].head(10).tolist()}")
