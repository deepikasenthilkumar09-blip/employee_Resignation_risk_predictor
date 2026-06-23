from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    joining_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    review_date = models.DateField(auto_now_add=True)
    rating = models.IntegerField() # 1-5
    comments = models.TextField()

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending') # Approved, Rejected, Pending

class ResignationPrediction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    input_data = models.JSONField()
    risk_score = models.FloatField()
    prediction_date = models.DateTimeField(auto_now_add=True)
    predicted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='predictions_made')
