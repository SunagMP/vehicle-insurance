import pandas as pd
from sklearn.model_selection import train_test_split
import os
from logger_file import create_logger

#--------- creating the logger instance
logger = create_logger(name="data_preprocessing_logger")

def split_the_data(df:pd.DataFrame, test_size:float):
    try:
        x = df.drop(columns=['Response'])
        y = df['Response']

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, stratify=y)
        train_data = pd.concat([x_train, y_train], axis=1)
        test_data = pd.concat([x_test, y_test], axis=1)
        logger.debug("data split into train and test data set successfully")
        return train_data, test_data
    
    except Exception as e:
        logger.error(f"failed to split the data , {e}")

def save_the_train_test_data(df:pd.DataFrame, dataset_name:str):
    try:
        os.makedirs('data', exist_ok=True)
        os.makedirs('./data/split', exist_ok=True)
        df.to_csv(f"data/split/{dataset_name}.csv", index=False)
        logger.debug("data save successfull")

    except Exception as e:
        logger.error(f"failed to save the split data, {e}")

def main():
    try :
        df = pd.read_csv('data/raw/raw_data.csv')

        test_size = 0.2
        train_data, test_data = split_the_data(df, test_size)
        save_the_train_test_data(train_data, "train_data")
        save_the_train_test_data(test_data, "test_data")

    except Exception as e:
        logger.error(f"data_preprocesssing failed due to , {e}")

if __name__ == '__main__':
    main()