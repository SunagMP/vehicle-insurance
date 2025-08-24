import pandas as pd
import os 
import pickle
import json

from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import PowerTransformer

from logger_file import create_logger

#-------- logger instance
logger = create_logger("train_evaluate_model_logger")


def create_model(n_estimators:int, max_depth):
    try:
        trf1 = ColumnTransformer([
            ('OHE_gender', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False), [0, 4])
        ], remainder='passthrough')

        trf2 = ColumnTransformer([
            ('PT-on-numerics', PowerTransformer(method='yeo-johnson'), [5, 6, 10])
        ], remainder='passthrough')

        rf = RandomForestClassifier(class_weight="balanced", n_estimators=n_estimators, max_depth=max_depth)

        pipe = Pipeline([
            ('OHE', trf1),
            ('powerTransformation', trf2),
            ('model', rf)
        ])

        logger.debug("model created")
        return pipe
    
    except Exception as e:
        logger.error(f"Failed to create the model. due to -> {e}")

def train_model(x:pd.DataFrame, y:pd.DataFrame, pipe):
    try:
        pipe.fit(x, y)
        logger.debug("model trained successfully")
        return pipe
    except Exception as e:
        logger.error(f"model training failed, due to -> {e}")

def save_model(pipe):
    try:
        os.makedirs('models', exist_ok=True)
        with open('models/model.pkl', 'wb') as f:
            pickle.dump(pipe, f)
        logger.debug("model save succcessfull")

    except Exception as e:
        logger.error(f"failed to save the model, {e}")

def load_model():
    try:
        with open('models/model.pkl', 'rb') as f:
            model = pickle.load(f)
        logger.debug("model loaded successfull")
        return model
    except Exception as e:
        logger.error(f"Model load failed, {e}")

def evaluate_model(x_test:pd.DataFrame, y_test:pd.DataFrame):
    try:
        model = load_model()
        y_pred = model.predict(x_test)

        accuracy = accuracy_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        logger.debug("Evaluation success")

        os.makedirs('metrics', exist_ok=True)
        with open('metrics/result.json', 'w') as f:
            json.dump({
                "accuracy": accuracy,
                "recall": recall,
                "f1_score": f1
            }, f, indent=4)
        logger.debug("evaluation saved to the files")
    
    except Exception as e:
        logger.error(f"Evaluation failed due to, {e}")

def main():
    try:
        n_estimators = 100
        max_depth = None
        pipe = create_model(n_estimators, max_depth)

        print("model-created")
        train_data = pd.read_csv('data/cleaned/train_data.csv')
        x_train = train_data.drop(columns=['Response'])
        y_train = train_data['Response']
        trained_model = train_model(x=x_train, y=y_train, pipe=pipe)

        print("model-trained")
        save_model(trained_model)

        print("model-saved")
        test_data = pd.read_csv('data/cleaned/test_data.csv')
        x_test = test_data.drop(columns=['Response'])
        y_test = test_data['Response']
        evaluate_model(x_test, y_test)


    except Exception as e:
        logger.error(f"train_evaluate failed due to -> {e}")

if __name__ == '__main__':
    main()