import pandas as pd
from pymongo import MongoClient
from utils import create_logger
import os

#------------ getting logger ---------------
logger = create_logger("data_ingestion_loger")

def establish_mongo_connection():
    try:
        client = MongoClient("mongodb+srv://sunag:ecvLQI5749CnB3Ss@cluster0.h57sogb.mongodb.net/")
        db = client["myDatabase"]
        collection = db["myCollection"]
        logger.debug("MongoDb Connection established successfully")
        return collection
    except Exception as e:
        logger.error(f"Couldn't establish the connection due to -> {e}")

def get_data_from_mongo(collection):
    try:
        data = list(collection.find())
        logger.debug("Data fetch successfull from mongoDB")

        df = pd.DataFrame(data)
        df = df.drop(columns=["_id"])
        logger.debug("Data gathered as dataframe successfully")
        return df
    except Exception as e:
        logger.error(f"Failed to get data due to , {e}")

def save_the_data(df:pd.DataFrame):
    try:
        os.makedirs('data', exist_ok=True)
        os.makedirs('./data/raw', exist_ok=True)
        
        df.to_csv('data/raw/raw_data.csv', index=False)
        logger.debug("Data saved to project directory")
    except Exception as e:
        logger.error(f"Failed to save the raw data , {e}")

def main():
    try:
        collection = establish_mongo_connection()
        df = get_data_from_mongo(collection)
        save_the_data(df)

    except Exception as e:
        logger.error(f"Data ingestion failed due to , {e}")

if __name__ == '__main__':
    main()