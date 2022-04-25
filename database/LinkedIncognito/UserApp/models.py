from email.policy import default
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
        'profile1.jpg', 'profile2.jpg', 'profile3.jpg', 'profile4.jpg', 'profile5.jpg', 
        'profile6.jpg', 'profile7.jpg', 'profile8.jpg', 'profile9.jpg', 'profile10.jpg', 
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uniqueId = models.CharField(null=True)
    # maybe remove upload_to??
    image = models.ImageField(default='default.png', upload_to='profile_images')
    email_confirmed = models.BooleanField(default=False)
    # rm?
    date_birth = models.DateField()
    # rm?
    sex = models.CharField(choices=SEX_CHOICES, default=OTHER)
    marital_status = models.CharField(choices=MARITAL_CHOICES, default=SINGLE)
    address_line1 = models.CharField(null=True)
    address_line2 = models.CharField(null=True)
    city = models.CharField(null=True)
    state = models.CharField(choices=STATE_CHOICES, default=NY)
    phone_number = models.CharField(null=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField()
    cover_letter = models.FileField(upload_to='resumes')
    cv = models.FileField(upload_to='resumes')

    def __str__(self):
        return '{} {} {}'.format(self.user.first_name, self.user.last_name, self.uniqueId)

    def get_absolute_url(self):
        return reverse('resume-detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Creating SlugField for the URL - to detailed page
        if self.slug is None:
            self.slug = slugify('{} {} {}'.format(self.user.first_name, self.user.last_name, self.user.uniqueId))

        # Creating a unique Identifier for the resume (useful for other things in the future)
        if self.uniqueId is None:
            self.uniqueId = 'user-'+str(uuid4()).split('-')[4]

        # assign a default profile image
        
    