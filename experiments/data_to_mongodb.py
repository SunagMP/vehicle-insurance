# mongodb+srv://sunag:ecvLQI5749CnB3Ss@cluster0.h57sogb.mongodb.net/

import pandas as pd
from pymongo import MongoClient

# Step 1: Read your CSV file
csv_file = "experiments/data.csv"
df = pd.read_csv(csv_file)

# Step 2: Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://sunag:ecvLQI5749CnB3Ss@cluster0.h57sogb.mongodb.net/")
db = client["myDatabase"]
collection = db["myCollection"]

# Step 3: Convert CSV into records
data = df.to_dict(orient="records")

# Step 4: Insert in batches
batch_size = 5000
for i in range(0, len(data), batch_size):
    batch = data[i:i+batch_size]
    collection.insert_many(batch)
    print(f"Inserted records {i+1} to {i+len(batch)}")

print("✅ All rows uploaded successfully!")
