from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
#class Applicants(models.Model):
#    Username = models.AutoField(primary_key=True)
#    Password = models.CharField(max_length=100)
#    Email = models.CharField(max_length=50)
#    FirstName = models.CharField(max_length=25)
#    LastName = models.CharField(max_length=25)
#    Degree = models.CharField(max_length=30)

#class Employers(models.Model):
#    Username = models.AutoField(primary_key=True)
#    Password = models.CharField(max_length=100)
#    Email = models.CharField(max_length=50)
#    FirstName = models.CharField(max_length=25)
#    LastName = models.CharField(max_length=25)
#    CompanyName = models.CharField(max_length=50)
#    ImplicitBiasFile = models.CharField(max_length=500)

#class JobPosting(models.Model):
#    Title = models.AutoField(primary_key=True)
#    JobType = models.CharField(max_length=20)
#    Description = models.CharField(max_length=1000)

# class Interview(models.Model):
#     Employer = models.ForeignKey(Employers.Username)
#     Applicant = models.ForeignKey(Applicants.Username)
#     Date = models.Date()
#     Time = models.Time()

# custom user model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, role, first_name, last_name, password):
        if not email:
            raise ValueError("Users must have email address.")
        if not username:
            raise ValueError("Users must have username.")
        if not role:
            raise ValueError("Users must have role.")
        if not first_name:
            raise ValueError("Users must enter first name.")
        if not last_name:
            raise ValueError("Users must enter last name.")
        if not password:
            raise ValueError("Users must have password.")                                                

        user = self.model(
            email = self.normalize_email(email),
            password=password,
            username = username,  
            role = role,
            first_name = first_name,
            last_name = last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user    

    def create_superuser(self, email, username, role, first_name, last_name, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            username = username,  
            role = role,
            first_name = first_name,
            last_name = last_name       
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user    




class Account(AbstractBaseUser):
    EMPLOYER = 'Employer'
    APPLICANT = 'Applicant'

    ROLE_CHOICES = [
        (EMPLOYER, 'Employer'),
        (APPLICANT, 'Applicant')
    ]

    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    # begin required
    username = models.CharField(max_length=100, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # end required
    first_name = models.CharField(max_length=100, default="Owner")
    last_name = models.CharField(max_length=100, default = "Owner")
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    uniqueId = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=APPLICANT)

    # allowing users to login using email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role', 'first_name', 'last_name']
    #REQUIRED_FIELDS = ['username']


    objects = MyAccountManager()

    def __str__(self):
        #return '{} {} {}'.format(self.first_name, self.last_name, self.uniqueId)
        return self.email

    # begin required
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    # end required

    def get_absolute_url(self):
        return reverse('public_profile', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Creating a unique Identifier for the user (useful for other things in the future) && a SlugField for the url
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[0]
        
        self.slug = slugify('{} {} {}'.format(self.first_name, self.last_name, self.uniqueId))

        super(Account, self).save(*args, **kwargs)
    






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
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    # might should change User to Company?
    # models.CASCADE means that if user gets deleted, the job will be deleted with them

    def __str__(self):
        return '{} looking for {}'.format(self.company, self.title)







# Currently unused, TRYING to get them to inherit from user class and be created upon registration but no luck so far
class Applicants(User):
    Degree = models.CharField(max_length=30)

class Employers(User):
    ImplicitBiasFile = models.CharField(max_length=500)

#from django.db import models
from django.template.defaultfilters import slugify
#from django.contrib.auth.models import User
#from django.utils import timezone
from uuid import uuid4
import random

class Resume(models.Model):
    # seems like we wont be using these LMFAO
    MALE = 'Male'
    FEMALE = 'Female'
    NONBINARY = 'Nonbinary'
    OTHER = 'Other'
    MARRIED = 'Married'
    SINGLE = 'Single'
    WIDOWED = 'Widowed'
    DIVORCED = 'Divorced'

    AK	= 'Alaska'
    AL	= 'Alabama'
    AR	= 'Arkansas'
    AZ	= 'Arizona'
    CA	= 'California'
    CO	= 'Colorado'
    CT	= 'Connecticut'
    DC	= 'District of Columbia'
    DE	= 'Delaware'
    FL	= 'Florida'
    GA	= 'Georgia'
    HI	= 'Hawaii'
    IA	= 'Iowa'
    ID	= 'Idaho'
    IL	= 'Illinois'
    IN	= 'Indiana'
    KS	= 'Kansas'
    KY	= 'Kentucky'
    LA	= 'Louisiana'
    MA	= 'Massachusetts'
    MD	= 'Maryland'
    ME	= 'Maine'
    MI	= 'Michigan'
    MN	= 'Minnesota'
    MO	= 'Missouri'
    MS	= 'Mississippi'
    MT	= 'Montana'
    NC	= 'North Carolina'
    ND	= 'North Dakota'
    NE	= 'Nebraska'
    NH	= 'New Hampshire'
    NJ	= 'New Jersey'
    NM	= 'New Mexico'
    NV	= 'Nevada'
    NY	= 'New York'
    OH	= 'Ohio'
    OK	= 'Oklahoma'
    OR	= 'Oregon'
    PA	= 'Pennsylvania'
    PR	= 'Puerto Rico'
    RI	= 'Rhode Island'
    SC	= 'South Carolina'
    SD	= 'South Dakota'
    TN	= 'Tennessee'
    TX	= 'Texas'
    UT	= 'Utah'
    VA	= 'Virginia'
    VT	= 'Vermont'
    WA	= 'Washington'
    WI	= 'Wisconsin'
    WV	= 'West Virginia'
    WY = 'Wyoming'

    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NONBINARY, 'Nonbinary'),
        (OTHER, 'Other'),
    ]

    MARITAL_CHOICES = [
        (MARRIED, 'Married'),
        (SINGLE, 'Single'),
        (WIDOWED, 'Widowed'),
        (DIVORCED, 'Divorced'),
    ]

    STATE_CHOICES = [
        (AK,'Alaska'),
        (AL,'Alabama'),
        (AR,'Arkansas'),
        (AZ,'Arizona'),
        (CA,'California'),
        (CO,'Colorado'),
        (CT,'Connecticut'),
        (DC,'District of Columbia'),
        (DE,'Delaware'),
        (FL,'Florida'),
        (GA,'Georgia'),
        (HI,'Hawaii'),
        (IA,'Iowa'),
        (ID,'Idaho'),
        (IL,'Illinois'),
        (IN,'Indiana'),
        (KS,'Kansas'),
        (KY,'Kentucky'),
        (LA,'Louisiana'),
        (MA,'Massachusetts'),
        (MD,'Maryland'),
        (ME,'Maine'),
        (MI,'Michigan'),
        (MN,'Minnesota'),
        (MO,'Missouri'),
        (MS,'Mississippi'),
        (MT,'Montana'),
        (NC,'North Carolina'),
        (ND,'North Dakota'),
        (NE,'Nebraska'),
        (NH,'New Hampshire'),
        (NJ,'New Jersey'),
        (NM,'New Mexico'),
        (NV,'Nevada'),
        (NY,'New York'),
        (OH,'Ohio'),
        (OK,'Oklahoma'),
        (OR,'Oregon'),
        (PA,'Pennsylvania'),
        (PR,'Puerto Rico'),
        (RI,'Rhode Island'),
        (SC,'South Carolina'),
        (SD,'South Dakota'),
        (TN,'Tennessee'),
        (TX,'Texas'),
        (UT,'Utah'),
        (VA,'Virginia'),
        (VT,'Vermont'),
        (WA,'Washington'),
        (WI,'Wisconsin'),
        (WV,'West Virginia'),
        (WY,'Wyoming'),
    ]

    IMAGES = [
        'profile-pic1.jpg', 'profile-pic2.jpg', 'profile-pic3.jpg', 'profile-pic4.jpg', 'profile-pic5.jpg', 
        'profile-pic6.jpg', 'profile-pic7.jpg', 'profile-pic8.jpg', 'profile-pic9.jpg', 'profile-pic10.jpg', 
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uniqueId = models.CharField(max_length=100, null=True, blank=True)
    # maybe remove upload_to??
    image = models.ImageField(default='default.png', upload_to='profile_images')
    email_confirmed = models.BooleanField(default=False)
    # rm?
    date_birth = models.DateField(blank=True, null=True)
    # rm?
    sex = models.CharField(max_length=100, choices=SEX_CHOICES, default=OTHER)
    marital_status = models.CharField(max_length=100, choices=MARITAL_CHOICES, default=SINGLE)
    address_line1 = models.CharField(max_length=100, null=True, blank=True)
    address_line2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default=NY)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(null=True, blank=True)
    cover_letter = models.FileField(upload_to='resumes', null=True, blank=True)
    cv = models.FileField(upload_to='resumes', null=True, blank=True)

    def __str__(self):
        return '{} {} {}'.format(self.user.first_name, self.user.last_name, self.uniqueId)

    def get_absolute_url(self):
        return reverse('resume-detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Creating a unique Identifier for the resume (useful for other things in the future) && a SlugField for the url
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[0]
        
        self.slug = slugify('{} {} {}'.format(self.user.first_name, self.user.last_name, self.user.uniqueId))

        # assign a default profile image
        if self.image is None:
            self.image = random.choice(self.IMAGES)

        super(Resume, self).save(*args, **kwargs)
    

class Education(models.Model):
    # theres more
    LEVEL5A = 'Some High School Education'
    LEVEL5B = 'High School Certificate (G.E.D.)'
    LEVEL5C = 'High School Diploma'
    LEVEL6A = 'Some College Education'
    LEVEL6B = "Associate's Degree (AS/AA)"
    LEVEL6C = "Bachelor's Degree (BS/BA)"
    LEVEL7A = 'Some Postgraduate School'
    LEVEL7B = 'Professional School Graduate'
    LEVEL7C = "Master's Degree (MS/MA)"
    LEVEL8 = "Doctorate's Degree (PHD)"

    LEVEL_CHOICES = [
        (LEVEL5A, 'Some High School Education'),
        (LEVEL5B, 'High School Certificate (G.E.D.)'),
        (LEVEL5C, 'High School Diploma'),
        (LEVEL6A, 'Some College Education'),
        (LEVEL6B, "Associate's Degree (AS/AA)"),
        (LEVEL6C, "Bachelor's Degree (BS/BA)"),
        (LEVEL7A, 'Some Postgraduate School'),
        (LEVEL7B, 'Professional School Graduate'),
        (LEVEL7C, "Master's Degree (MS/MA)"),
        (LEVEL8, "Doctorate Degree (PHD)"),
    ]


    institution = models.CharField(null=True, blank=True, max_length=200)
    qualification = models.CharField(null=True, blank=True, max_length=200)
    level = models.CharField(choices=LEVEL_CHOICES, default=LEVEL5A, max_length=200)
    start_date = models.DateField(null=True, blank=True)
    graduated = models.DateField(blank=True, null=True)
    major_subject = models.CharField(null=True, blank=True, max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    def __str__(self):
        return '{} for {} {}'.format(self.qualification, self.resume.user.first_name, self.resume.user.last_name)
    

from django.contrib.postgres.fields import ArrayField

class Experience(models.Model):
    company = models.CharField(null=True, blank=True, max_length=200)
    position = models.CharField(null=True, blank=True, max_length=200)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    skills = ArrayField(models.CharField(max_length=100, null=True, blank=True), default=list)
    date_created = models.DateTimeField(default=timezone.now)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return '{} at {}'.format(self.position, self.company)
    