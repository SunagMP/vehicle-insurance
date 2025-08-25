import os
import pytest

def test_data_ingestion_artifact():
    assert os.path.exists("data/raw"), "Raw data not found!"

def test_data_preprocessing_artifact():
    assert os.path.exists("data/split"), "Split data not found!"

def test_feature_engineering_artifact():
    assert os.path.exists("data/cleaned"), "Cleaned data not found!"

def test_model_artifact():
    assert os.path.exists("models/model.pkl"), "Model not found!"

def test_metrics_artifact():
    assert os.path.exists("metrics/result.json"), "Metrics not found!"
