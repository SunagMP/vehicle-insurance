# 🚗 Vehicle Insurance Predictor (with CI/CD Pipeline)

This project is an **industry-grade Machine Learning application** that predicts whether an insurance policy can be provided to a customer or not. The solution is built with modular coding practices, experiment tracking, CI/CD automation, and a FastAPI endpoint for deployment.

---

## 📌 Features
- **Random Forest Classifier** for classification task.  
- **End-to-End ML Pipeline** using `dvc.yaml`.  
- **Data ingestion** from MongoDB cluster.  
- **Automated preprocessing & feature engineering**.  
- **Model training & evaluation** with results logged.  
- **Experiment tracking & versioning** using **MLflow** & **DVC**.  
- **FastAPI Endpoint** for serving predictions.  
- **CI/CD Pipeline** via **GitHub Actions** for continuous integration and deployment.  
- **Logging & Error Handling** with Python’s `logging` module.  

---

## 🏗️ Project Pipeline
The ML pipeline is fully modular and defined in `dvc.yaml`.  

1. **Data Ingestion**  
   - Connects to **MongoDB Atlas** cluster.  
   - Fetches raw data and stores it locally.  

2. **Data Preprocessing**  
   - Applies preprocessing steps.  
   - Splits dataset into **train-test** sets.  

3. **Feature Engineering**  
   - Creates new meaningful features.  
   - Cleans and saves the **finalized dataset**.  

4. **Model Training & Evaluation**  
   - Trains a **Random Forest Classifier**.  
   - Evaluates performance on test data.  
   - Saves trained model and results.  

5. **FastAPI Service**  
   - Provides an endpoint `/predict` for user input.  
   - Returns predictions on whether insurance can be provided.  

---
## ⚙️ Tech Stack
- **Python** (Modular coding practices)  
- **Random Forest Classifier (Scikit-learn)**  
- **MongoDB** (Data Storage)  
- **FastAPI** (Serving predictions)  
- **DVC** (Pipeline orchestration & data versioning)  
- **MLflow** (Experiment tracking)  
- **Git & GitHub Actions** (CI/CD automation)  
- **Logging & OS modules** (System management & debugging)  

---

## 🚀 CI/CD Workflow
- Triggered automatically on **push to main** branch.  
- Runs **tests, linting, training, and evaluation**.  
- Deploys updated model with FastAPI service.  

---

## 🔧 Installation & Usage

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/vehicle-insurance-predictor.git
cd vehicle-insurance-predictor


2. **Create Virtual Environment and Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
