import sqlite3
import pandas as pd

conn = sqlite3.connect('fda_recalls.db')
df = pd.read_csv('results/clean_data.csv')
df.to_sql('recalls', conn, if_exists='replace', index=False)
conn.close()
print(f"Loaded {len(df)} records into fda_recalls.db")
