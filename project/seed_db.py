import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_management.settings')
django.setup()

from django.contrib.auth.models import User
from portal.models import Employee

def seed_data():
    # Create superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' created (pass: admin123)")
    
    first_names = ["John", "Jane", "Robert", "Emily", "Michael", "Sarah", "David", "Jessica", "William", "Linda", 
                  "James", "Elizabeth", "Joseph", "Karen", "Thomas", "Nancy", "Christopher", "Betty", "Charles", "Margaret"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                 "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
    depts = ["Engineering", "HR", "Sales", "Marketing", "Finance", "Legal"]
    roles = ["Senior Developer", "HR Manager", "Sales Exec", "Marketing Lead", "Financial Analyst", "Backend Engineer"]
    
    # Create 20 employees
    for i in range(20):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        username = f"{fname.lower()}.{lname.lower()}.{random.randint(10,99)}"
        eid = f"EMP{100 + i}"
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, password='password123', 
                                         first_name=fname, last_name=lname)
            Employee.objects.create(
                user=user, 
                employee_id=eid, 
                department=random.choice(depts), 
                job_role=random.choice(roles), 
                salary_range=random.choice(['Low', 'Medium', 'High'])
            )
            print(f"Created Employee: {username}")

if __name__ == '__main__':
    seed_data()
