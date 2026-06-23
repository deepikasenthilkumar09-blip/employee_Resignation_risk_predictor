from django import forms
from .models import Employee
from django.contrib.auth.models import User

class ResignationRiskForm(forms.Form):
    age = forms.IntegerField(label='Age', min_value=18, max_value=70, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    monthly_income = forms.IntegerField(label='Monthly Income ($)', min_value=1000, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    total_working_years = forms.IntegerField(label='Total Working Years', min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    years_at_company = forms.IntegerField(label='Years at Company', min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    years_in_current_role = forms.IntegerField(label='Years in Current Role', min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    job_level = forms.ChoiceField(label='Job Level', choices=[(str(i), str(i)) for i in range(1, 6)], widget=forms.Select(attrs={'class': 'form-control'}))
    job_satisfaction = forms.ChoiceField(label='Job Satisfaction', choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High'), ('4', 'Very High')], widget=forms.Select(attrs={'class': 'form-control'}))
    env_satisfaction = forms.ChoiceField(label='Environment Satisfaction', choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High'), ('4', 'Very High')], widget=forms.Select(attrs={'class': 'form-control'}))
    work_life_balance = forms.ChoiceField(label='Work Life Balance', choices=[('1', 'Bad'), ('2', 'Good'), ('3', 'Better'), ('4', 'Best')], widget=forms.Select(attrs={'class': 'form-control'}))
    overtime = forms.BooleanField(label='Does the employee work Overtime?', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class AddEmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    employee_id = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    job_role = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    salary_range = forms.ChoiceField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], widget=forms.Select(attrs={'class': 'form-control'}))
