import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def train_ibm_model():
    url = "https://raw.githubusercontent.com/nelson-wu/employee-attrition-ml/master/WA_Fn-UseC_-HR-Employee-Attrition.csv"
    print("Downloading IBM HR Dataset...")
    df = pd.read_csv(url)
    
    # Preprocessing
    # Target variable: Attrition (Yes/No)
    le = LabelEncoder()
    df['Attrition'] = le.fit_transform(df['Attrition']) # Yes=1, No=0
    
    # Drop irrelevant columns
    df = df.drop(['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber'], axis=1)
    
    # Handling categorical variables for a subset of features we will use in the form
    # We'll pick top features to keep the form user-friendly
    features = [
        'Age', 'MonthlyIncome', 'TotalWorkingYears', 'YearsAtCompany', 
        'YearsInCurrentRole', 'JobLevel', 'JobSatisfaction', 
        'EnvironmentSatisfaction', 'OverTime', 'WorkLifeBalance'
    ]
    
    X = df[features].copy()
    X['OverTime'] = le.fit_transform(X['OverTime']) # Yes=1, No=0
    y = df['Attrition']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model
    model_path = os.path.join('portal', 'resignation_model.joblib')
    joblib.dump(model, model_path)
    
    print(f"IBM HR Model trained and saved to {model_path}")
    print(f"Accuracy: {model.score(X_test, y_test):.2f}")
    
    # Save feature names to ensure consistency in predictions
    joblib.dump(features, os.path.join('portal', 'features.joblib'))

if __name__ == '__main__':
    train_ibm_model()
