import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Create dummy data for training
def generate_data(n=2000):
    np.random.seed(42)
    satisfaction = np.random.uniform(0.1, 1.0, n)
    last_eval = np.random.uniform(0.3, 1.0, n)
    num_projects = np.random.randint(2, 8, n)
    avg_hours = np.random.randint(100, 320, n)
    time_company = np.random.randint(2, 10, n)
    accident = np.random.choice([0, 1], n, p=[0.85, 0.15])
    promotion = np.random.choice([0, 1], n, p=[0.98, 0.02])
    salary = np.random.choice([0, 1, 2], n) # 0:low, 1:medium, 2:high
    
    # Target: Attrition (simplified logic for correlation)
    # Risk increases if satisfaction is low, hours are very high, or no promotion
    risk = (1.0 - satisfaction) * 0.6 + (avg_hours / 320) * 0.2 + (1 - promotion) * 0.1 + (2 - salary) * 0.1
    attrition = (risk > 0.6).astype(int)
    
    df = pd.DataFrame({
        'satisfaction_level': satisfaction,
        'last_evaluation': last_eval,
        'number_project': num_projects,
        'average_montly_hours': avg_hours,
        'time_spend_company': time_company,
        'Work_accident': accident,
        'promotion_last_5years': promotion,
        'salary': salary,
        'attrition': attrition
    })
    return df

data = generate_data()

X = data.drop('attrition', axis=1)
y = data['attrition']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
model_path = os.path.join('portal', 'resignation_model.joblib')
joblib.dump(model, model_path)

print(f"Model trained and saved to {model_path}")
print(f"Accuracy on test set: {model.score(X_test, y_test):.2f}")
