import joblib
import os
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
from .models import Employee, ResignationPrediction, PerformanceReview
from .forms import ResignationRiskForm, AddEmployeeForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

# Load the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'resignation_model.joblib')
try:
    model = joblib.load(MODEL_PATH)
except:
    model = None

@login_required
def dashboard(request):
    employees_count = Employee.objects.count()
    predictions = ResignationPrediction.objects.order_by('-prediction_date')[:5]
    
    # Simple stats for charts
    labels = ['Low Risk', 'High Risk']
    high_risk_count = ResignationPrediction.objects.filter(risk_score__gt=0.5).count()
    low_risk_count = ResignationPrediction.objects.filter(risk_score__lte=0.5).count()
    chart_data = [low_risk_count, high_risk_count]
    
    context = {
        'employees_count': employees_count,
        'predictions': predictions,
        'chart_labels': labels,
        'chart_data': chart_data,
    }
    return render(request, 'portal/dashboard.html', context)

@login_required
def predict_risk(request):
    prediction = None
    risk_score = None
    if request.method == 'POST':
        form = ResignationRiskForm(request.POST)
        if form.is_valid():
            # Match features exactly as defined in train_ibm_model.py
            # features = ['Age', 'MonthlyIncome', 'TotalWorkingYears', 'YearsAtCompany', 'YearsInCurrentRole', 'JobLevel', 'JobSatisfaction', 'EnvironmentSatisfaction', 'OverTime', 'WorkLifeBalance']
            data = {
                'Age': [form.cleaned_data['age']],
                'MonthlyIncome': [form.cleaned_data['monthly_income']],
                'TotalWorkingYears': [form.cleaned_data['total_working_years']],
                'YearsAtCompany': [form.cleaned_data['years_at_company']],
                'YearsInCurrentRole': [form.cleaned_data['years_in_current_role']],
                'JobLevel': [int(form.cleaned_data['job_level'])],
                'JobSatisfaction': [int(form.cleaned_data['job_satisfaction'])],
                'EnvironmentSatisfaction': [int(form.cleaned_data['env_satisfaction'])],
                'OverTime': [1 if form.cleaned_data['overtime'] else 0],
                'WorkLifeBalance': [int(form.cleaned_data['work_life_balance'])]
            }
            df = pd.DataFrame(data)
            
            if model:
                risk_score = model.predict_proba(df)[0][1]
                prediction = "High Risk" if risk_score > 0.4 else "Low Risk" # Lower threshold for IBM data normally
                
                # Log the prediction
                ResignationPrediction.objects.create(
                    input_data=data,
                    risk_score=risk_score,
                    predicted_by=request.user
                )
    else:
        form = ResignationRiskForm()
        
    return render(request, 'portal/predict.html', {'form': form, 'prediction': prediction, 'risk_score': risk_score})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'portal/login.html', {'form': form})

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'portal/employee_list.html', {'employees': employees})

@login_required
def analytics(request):
    # Aggregated metrics for Power-BI style dashboard
    total_emp = Employee.objects.count()
    total_preds = ResignationPrediction.objects.count()
    high_risk = ResignationPrediction.objects.filter(risk_score__gt=0.5).count()
    
    # Dept-wise distribution
    depts = ['Engineering', 'HR', 'Sales', 'Marketing', 'Finance']
    dept_counts = [Employee.objects.filter(department=d).count() for d in depts]
    
    # Prediction trend (last 7 days example)
    from django.utils import timezone
    from datetime import timedelta
    labels = []
    daily_risks = []
    for i in range(6, -1, -1):
        date = timezone.now().date() - timedelta(days=i)
        labels.append(date.strftime('%b %d'))
        count = ResignationPrediction.objects.filter(prediction_date__date=date, risk_score__gt=0.5).count()
        daily_risks.append(count)

    context = {
        'total_emp': total_emp,
        'total_preds': total_preds,
        'high_risk': high_risk,
        'dept_labels': depts,
        'dept_data': dept_counts,
        'trend_labels': labels,
        'trend_data': daily_risks,
    }
    return render(request, 'portal/analytics.html', context)

@login_required
def export_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="hr_data_for_powerbi.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Prediction ID', 'Risk Score', 'Date', 'Dept', 'Job Role'])
    
    preds = ResignationPrediction.objects.all()
    for p in preds:
        # Note: input_data might need parsing depending on structure
        dept = p.input_data.get('department', ['N/A'])[0] if isinstance(p.input_data, dict) else 'N/A'
        writer.writerow([p.id, p.risk_score, p.prediction_date, dept, 'N/A'])
    
    return response

@login_required
def add_employee(request):
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            # Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password='password123' # Default password
            )
            # Create Employee
            Employee.objects.create(
                user=user,
                employee_id=form.cleaned_data['employee_id'],
                department=form.cleaned_data['department'],
                job_role=form.cleaned_data['job_role'],
                salary_range=form.cleaned_data['salary_range']
            )
            return redirect('employee_list')
    else:
        form = AddEmployeeForm()
    return render(request, 'portal/add_employee.html', {'form': form})
