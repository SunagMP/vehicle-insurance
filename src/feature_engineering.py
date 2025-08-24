import pandas as pd
import os

from logger_file import create_logger

#------------ create logging instance
logger = create_logger("feature_engineering_logger")

#----------- utility functions
def age_group(age):
    if age>=0 and age<=30:
        return 0
    elif age>=31 and age<=50:
        return 1
    return 2

def premium_range(amount):
    if amount>0 and amount<=50000:
        return 0
    elif amount>=50001 and amount<=150000:
        return 1
    return 2

def vehicle_age(age):
    if age == "1-2 Year":
        return 0 #39997
    elif age == "< 1 Year": #
        return 1
    return 2

#----------- create methods
def create_features(df:pd.DataFrame):
    try:
        df['Age_Group'] = df['Age'].map(age_group)
        df['Old_Damaged_vehicle'] = ((df['Vehicle_Age'] == '> 2 Years')&(df['Vehicle_Damage'] == "Yes")).astype(int)
        df['Premium_Range'] = df['Annual_Premium'].map(premium_range)
        df['Premium_Per_Vintage'] = df['Annual_Premium']/df['Vintage']
        df['Vehicle_Age'] = df['Vehicle_Age'].map(vehicle_age)
        logger.debug("features created successfully")
        return df

    except Exception as e:
        logger.error("failed to create features due to , ", e)

def save_the_cleaned_data(df:pd.DataFrame, dataset_name:str):
    try:
        os.makedirs('data', exist_ok=True)
        os.makedirs('./data/cleaned', exist_ok=True)
        df = df.drop(columns=['id','Region_Code', 'Age', 'Annual_Premium'])
        df.to_csv(f"data/cleaned/{dataset_name}.csv", index=False)
        
    except Exception as e:
        logger.error("failed to save the split data, ", e)

def main():
    try:
        train_data = pd.read_csv('data/split/train_data.csv')
        train_data = create_features(train_data)
        logger.debug("features created for train dataset")
        save_the_cleaned_data(train_data, "train_data")
        logger.debug("train cleaned data is saved")

        test_data = pd.read_csv('data/split/test_data.csv')
        test_data = create_features(test_data)
        logger.debug("features created for test dataset")
        save_the_cleaned_data(test_data, "test_data")
        logger.debug("test cleaned data is saved")

    except Exception as e:
        logger.error("feature_engineering failed due to, ", e)

if __name__ == '__main__':
    main()