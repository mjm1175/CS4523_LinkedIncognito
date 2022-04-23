from email.policy import default
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Applicants(models.Model):
    Username = models.AutoField(primary_key=True)
    Password = models.CharField(max_length=100)
    Email = models.CharField(max_length=50)
    FirstName = models.CharField(max_length=25)
    LastName = models.CharField(max_length=25)
    Degree = models.CharField(max_length=30)

class Employers(models.Model):
    Username = models.AutoField(primary_key=True)
    Password = models.CharField(max_length=100)
    Email = models.CharField(max_length=50)
    FirstName = models.CharField(max_length=25)
    LastName = models.CharField(max_length=25)
    CompanyName = models.CharField(max_length=50)
    ImplicitBiasFile = models.CharField(max_length=500)

class JobPosting(models.Model):
    Title = models.AutoField(primary_key=True)
    JobType = models.CharField(max_length=20)
    Description = models.CharField(max_length=1000)

# class Interview(models.Model):
#     Employer = models.ForeignKey(Employers.Username)
#     Applicant = models.ForeignKey(Applicants.Username)
#     Date = models.Date()
#     Time = models.Time()


# Example model
class Job(models.Model):
    # these values are what will actually be stored in the database
    FULL_TIME = 'FT'
    PART_TIME = 'PT'
    REMOTE = 'RT'
    TIER1 = 't1'
    TIER2 = 't2'
    TIER3 = 't3'
    TIER4 = 't4'
    TIER5 = 't5'
    
    # Pairing backend values with front end displays
    TYPE_CHOICES = [
        (FULL_TIME, 'Full Time'),
        (PART_TIME, 'Part Time'),
        (REMOTE, 'Remote'),
    ]
    EXP_CHOICES = [
        (TIER1, 'Less than 2yrs'),
        (TIER2, '2yrs - 5yrs'),
        (TIER3, '5yrs - 10yrs'),
        (TIER4, '10yrs - 15yrs'),
        (TIER5, 'More than 15yrs'),
    ]

    title = models.CharField(max_length=150)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    salary = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=FULL_TIME)
    experience = models.CharField(max_length=10, choices=EXP_CHOICES, default=TIER1)
    summary = models.TextField()
    description = models.TextField()
    requirements = models.TextField()
    logo = models.ImageField(default='default-job.png', upload_to='upload_images')
    date_created = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # might should change User to Company?
    # models.CASCADE means that if user gets deleted, the job will be deleted with them

    def __str__(self):
        return '{} looking for {}'.format(self.company, self.title)


from django import forms
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
                    max_length=100,
                    required=True,
                    help_text='Enter Email Address',
                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                    )
    
    #first_name = forms.CharField(
    #                max_length=100,
    #                required=True,
    #                help_text='Enter First Name',
    #                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    #                )

    #last_name = forms.CharField(
    #                max_length=100,
    #                required=True,
    #                help_text='Enter Last Name',
    #                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}),
    #                )

    name = forms.CharField(
                    max_length=100,
                    required=True,
                    help_text='Enter Your Name',
                    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'})
                    )
    username = forms.CharField(
                    max_length=200,
                    #required=True,
                    help_text='Enter Username',
                    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'})
                    )
    password1 = forms.CharField(
                    help_text='Enter Password',
                    required=True,
                    widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
                    )

    password2 = forms.CharField(
                    #required=True,
                    help_text='Enter Password Again',
                    widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Repeat Password'}),
                    )

    check = forms.BooleanField(
                    #required=True
                    )

    class Meta:
        model = User
        fields = [
            #'usesrname', 'email', 'first_name', 'last_name', 'password1', 'password2', 'check',
            'name', 'email', 'password1',
        ]