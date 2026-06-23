# Employee Resignation Portal (HR Insight Pro)
A modern, full-stack Django application designed for HR departments to manage employee data and proactively predict resignation risks using Machine Learning.
## 🚀 Features
- **Dashboard & Overview:** Real-time summary of total employees, recent predictions, and risk distribution.
- **Employee Management:** Centralized system to add, view, and manage employee profiles and departmental roles.
- **AI-Powered Resignation Prediction:** Integrated Machine Learning module trained on IBM HR Analytics data to calculate resignation probability scores.
- **Interactive Analytics:** Visualized insights using Chart.js, including department-wise distributions and high-risk trends.
- **Data Export:** Generate CSV reports of risk analysis for integration with external BI tools (like Power BI or Tableau).
- **Secure Authentication:** Role-based access with secure login and session management.
## 🛠️ Tech Stack
- **Framework:** Django 5.x+
- **Frontend:** HTML, CSS (Vanilla), Bootstrap 4
- **Database:** SQLite (Default)
- **Machine Learning:** Scikit-learn, Pandas, Joblib
- **Visualization:** Chart.js
- **Icons & Styling:** Font Awesome, Google Fonts
## 📋 Installation & Setup
### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.
### 2. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
```
### 3. Install Dependencies
```bash
pip install django django-bootstrap4 pandas scikit-learn joblib
```
### 4. Database Setup
Run the migrations to set up the database schema:
```bash
python manage.py migrate
```
### 5. Seed the Database (Optional)
To populate the system with administrative credentials and sample employee data:
```bash
python seed_db.py
```
*Default Credentials Created:*
- **Username:** `admin`
- **Password:** `admin123`
## 🏃 How to Run
1. Start the development server:
   ```bash
   python manage.py runserver
   ```
2. Open your browser and navigate to: `http://127.0.0.1:8000/`
3. Log in using the admin credentials or register a new account.
## 🤖 Machine Learning Module
The project includes a pre-trained model located at `portal/resignation_model.joblib`. 
### Key Features used for Prediction:
- Age
- Monthly Income
- Total Working Years
- Years at Company
- Years in Current Role
- Job Level & Satisfaction
- OverTime & Work-Life Balance
If you wish to retrain the model with fresh data, use:
```bash
python train_model.py
```
## 📊 Analytics Dashboard
The portal features a Power-BI style analytics page that provides:
- High-Risk Employee Trends.
- Departmental Headcount.
- Growth Metrics and Recent Prediction Activity.
## 📂 Project Structure
- `hr_management/`: Main project settings and configurations.
- `portal/`: Primary application logic (Views, Models, Templates, Forms).
- `static/`: Global CSS, JavaScript, and Image assets.
- `seed_db.py`: Database initialization script.
- `train_model.py`: Training script for the ML model.
---
**Developed for HR Excellence.**
