from django.db import models

# Create your models here.

# Store department details
class Departments(models.Model):
    DepartmentId = models.AutoField(primary_key=True, serialize=True)
    DepartmentName = models.CharField(max_length=500)

# Store employee details
class Employees(models.Model):
    EmployeeId = models.AutoField(primary_key=True, serialize=True)
    EmployeeName = models.CharField(max_length=500)
    Department = models.CharField(max_length=500)
    DateOfJoining = models.DateField()
    PhotoFileName = models.CharField(max_length=500)