from urllib import request
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pytz import timezone
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from UserApp.models import Applicants, Employers, JobPosting
from UserApp.serializers import ApplicantSerializer, EmployerSerializer, JobPostingSerializer

from django.core.files.storage import default_storage
# Create your views here.


@csrf_exempt
def SaveFile(request):
        file=request.FILES['file']
        file_name=default_storage.save(file.name, file)
        return JsonResponse(file_name, safe=False)


from django.contrib.auth import login, authenticate
from .forms import AnonForm, ApplicationForm, CreateCompanyForm, CreateJobForm, FilterApplicantsForm, FilterJobsForm, RegisterForm, ResumeForm, SearchJobsForm

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {'form' : form}
        return render(request, 'register.html', context)

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('yes')
            form.save()
            user = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            messages.success(request, 'Account was created for ' + user)
            login(request, account)
            return redirect('home_page')
        else:
            print('no')
            print(form.errors)
            messages.error(request, 'Error processing your request')
            context = {'form': form}
            return render(request, 'register.html', context)

    return render(request, 'register.html', {})


@csrf_protect
def public_profile(request, slug):
    obj = Account.objects.get(slug=slug)

    educations = Education.objects.filter(resume=obj.resume)
    experiences = Experience.objects.filter(resume=obj.resume)

    context = {}
    context['object'] = obj
    context['educations'] = educations
    context['experiences'] = experiences    

    return render(request, 'public_profile.html', context)

@csrf_protect
def job_post(request, slug):
    obj = Job.objects.get(slug=slug)

    context = {}
    context['job'] = obj  

    return render(request, 'job_post.html', context)


##############################
# NEW NOT YET IN VSERVER
#############################

def company_detail(request, slug):
    obj = Company.objects.get(slug=slug)
    # getting all jobs whose company's slug matches this slug
    # (all jobs in this company)
    jobs = Job.objects.filter(company__slug=slug)

    context = {}
    context['company'] = obj
    context['jobs'] = jobs

    return render(request, 'company_detail.html', context)


def job_post_creation(request):
    if request.method == 'GET':
        form = CreateJobForm()
        context = {'form' : form}
        return render(request, 'job_post_creation.html', context)

    if request.method == 'POST':
        form = CreateJobForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            # might throw error
            obj.company = request.user.company
            obj.save()
            messages.success(request, 'Job post created successfully.')

            return redirect('job_post', slug=obj.slug)

        else:
            messages.error(request, 'Error processing your request')
            context = {'form': form}
            return render(request, 'job_post_creation.html', context)

    return render(request, 'job_post_creation.html', {})


def delete_experience(request, pk):
    exp = Experience.objects.get(pk=pk)

    if request.method == 'POST':
        exp.delete()
        messages.success(request, 'Experience deleted successfully')
        slug = request.user.resume.slug
        return redirect('resume_detail', slug=slug)

    return render(request, 'resume_detail.html', {'exp': exp})


def delete_education(request, pk):
    edu = Education.objects.get(pk=pk)

    if request.method == 'POST':
        edu.delete()
        messages.success(request, 'Education deleted successfully')
        slug = request.user.resume.slug
        return redirect('resume_detail', slug=slug)

    return render(request, 'resume_detail.html', {'edu': edu})


from django.http import FileResponse

def download(request, id, attrib_name):
    obj = Resume.objects.get(pk=id)
    if attrib_name == 'cover_letter':
        filename = obj.cover_letter.path
    elif attrib_name == 'cv':
        filename = obj.cv.path
    response = FileResponse(open(filename, 'rb'))
    return response 


@login_required
def company_creation(request, comp_id=None):
    if request.method == 'POST':
        if comp_id:
            comp = Company.objects.get(pk=comp_id)
            form = CreateCompanyForm(request.POST, request.FILES, instance=comp)
        else:
            form = CreateCompanyForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            obj.save()
            messages.success(request, 'Company profile updated successfully.')

            return redirect('profile')

        else:
            messages.error(request, 'Error processing your request')
            context = {'form': form}
            return render(request, 'company_creation.html', context)    

    if request.method == 'GET':
        if comp_id:
            comp = Company.objects.get(pk=comp_id)
            form = CreateCompanyForm(instance=comp)
        else:
            form = CreateCompanyForm()
        context = {'form' : form}
        return render(request, 'company_creation.html', context)

    return render(request, 'company_creation.html', {})


def search(request):
    job_search_form = SearchJobsForm()

    job_list = Job.objects.all()

    context = {}
    context['job_search_form'] = job_search_form
    context['jobs'] = job_list

    if request.method == 'POST':
        job_search_form = SearchJobsForm(request.POST)
        if job_search_form.is_valid():
            search = job_search_form.cleaned_data.get('title')
            jobs = []
            if len(search.split()) > 1:
                search_list = search.split()
                item_list = []
                for item in search_list:
                    a_list = Job.objects.filter(title__icontains=item)
                    for x in a_list:
                            item_list.append(x)
                [jobs.append(x) for x in item_list if x not in jobs]

            else:
                jobs = Job.objects.filter(title__icontains=search)

            context['jobs'] = jobs
            context['title'] = search

            # only sending jobs that fit the search
            return render(request, 'home.html', context)
    
        else:
            messages.error(request, 'Error processing your request')
            context['job_search_form'] = job_search_form
            return render(request, 'home.html', context)
    
    return None


def apply(request, slug):
    job = Job.objects.get(slug=slug)
    context = {}
    context['job'] = job

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)

            # setting foreign keys
            obj.applicant = request.user
            obj.job = job

            # setting upload fields
            # could also check for if upload_resume is None
            if form.cleaned_data.get('use_profile_resume') == 'Yes':
                obj.resume = request.user.resume.cv
            
            if form.cleaned_data.get('use_profile_cover_letter') == 'Yes':
                obj.resume = request.user.resume.cover_letter

            obj.save()
            messages.success(request, 'Application submitted successfully.')

            return redirect('home_page')

        else:
            messages.error(request, 'Error processing your request')
            context = {'form': form}
            return render(request, 'job_application.html', context)    

    if request.method == 'GET':
        form = ApplicationForm()
        context = {'form' : form}
        return render(request, 'job_application.html', context)

    return render(request, 'job_application.html', context)

@csrf_protect
def public_profile(request, slug):
    # search
    job_search_form = SearchJobsForm()

    context = {}
    context['job_search_form'] = job_search_form

    search_request = search(request)
    if search_request is not None:
        return search_request
    # end search

    obj = Account.objects.get(slug=slug)

    try:
        if obj.resume:
            educations = Education.objects.filter(resume=obj.resume)
            experiences = Experience.objects.filter(resume=obj.resume)

            # essentially only true if theyre an employer and have this set up
            if obj.resume.company is not None:
                jobs = Job.objects.filter(company=obj.resume.company)
                context['postings'] = jobs

            context['educations'] = educations
            context['experiences'] = experiences    
    except Account.resume.RelatedObjectDoesNotExist:
        pass


    context['object'] = obj

    return render(request, 'public_profile.html', context)


def view_applications(request, slug):
    # passing slug of the job posting
    job = Job.objects.get(slug=slug)
    apps = Application.objects.filter(job=job)

    context = {}
    context['job'] = job
    context['apps'] = apps

    return render(request, 'view_applications.html', context)



def job_post_creation(request, job_id=None):
    # search
    job_search_form = SearchJobsForm()

    context = {}
    context['job_search_form'] = job_search_form

    if request.method == 'GET':
        if job_id:
            job = Job.objects.get(pk=job_id)
            form = CreateJobForm(instance=job)
        else:
            form = CreateJobForm()

        context['form'] = form
        return render(request, 'job_post_creation.html', context)

    if request.method == 'POST':
        if job_id:
            job = Job.objects.get(pk=job_id)
            form = CreateJobForm(request.POST, instance=job)
        else:
            form = CreateJobForm(request.POST)

        search_request = search(request)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            # might throw error
    #			if request.user.resume: (check for this some better way)
            obj.company = request.user.resume.company
            obj.save()
            messages.success(request, 'Job post created successfully.')

            return redirect('job_post', slug=obj.slug)
        elif search_request is not None:
            return search_request
        else:
            messages.error(request, 'Error processing your request')
            context['form'] = form
            return render(request, 'job_post_creation.html', context)

    return render(request, 'job_post_creation.html', context)

def delete_job(request, pk):
    job = Job.objects.get(pk=pk)  

    if request.method == 'POST':        
        job.delete()                   
        messages.success(request, 'Job post deleted successfully')
        return redirect('profile')            

    return render(request, 'view_applications.html', {'job': job})

def download_from_application(request, id, attrib_name):
    obj = Application.objects.get(pk=id)
    if attrib_name == 'cover_letter':
        filename = obj.cover_letter.path
    elif attrib_name == 'resume':
        filename = obj.resume.path
    response = FileResponse(open(filename, 'rb'))
    return response 


def apply(request, slug, app_id=None):
    job = Job.objects.get(slug=slug)
    context = {}
    context['job'] = job

    if request.method == 'POST':
        if app_id:
            app = Application.objects.get(pk=app_id)
            form = ApplicationForm(request.POST, request.FILES, instance=app)
        else:
            form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)

            # setting foreign keys
            obj.applicant = request.user
            obj.job = job

            # setting upload fields
            # could also check for if upload_resume is None
            # if this works we can change upload_resume to be resume
            if form.cleaned_data.get('use_profile_resume') == 'Yes':
                obj.resume = request.user.resume.cv
            
            if form.cleaned_data.get('use_profile_cover_letter') == 'Yes':
                obj.cover_letter = request.user.resume.cover_letter

            obj.save()
            messages.success(request, 'Application submitted successfully.')

            return redirect('home_page')

        else:
            messages.error(request, 'Error processing your request')
            context['form'] = form
            return render(request, 'job_application.html', context)    

    if request.method == 'GET':
        if app_id:
            app = Application.objects.get(pk=app_id)
            form = ApplicationForm(instance=app)
        else:
            form = ApplicationForm()

        context['form'] = form
        return render(request, 'job_application.html', context)

    return render(request, 'job_application.html', context)

def delete_application(request, pk):
    app = Application.objects.get(pk=pk)  

    if request.method == 'POST':        
        app.delete()                   
        messages.success(request, 'Application deleted successfully')
        return redirect('profile')            

    return render(request, 'my_applications.html', {'app': app})


def my_applications(request):
    apps = Application.objects.filter(applicant=request.user)

    context = {}
    context['apps'] = apps

    return render(request, 'my_applications.html', context)    


# user views

from .functions import *

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {'form' : form}
        return render(request, 'register.html', context)

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            obj = form.save()

            # send validation email
            to_email = form.cleaned_data.get('email')
            welcome = WelcomeEmail(obj.uniqueId)
            e_mail = welcome.email()
            print(obj.uniqueId)
            send_email(e_mail, welcome.subject, [to_email])

            user = form.cleaned_data.get('username')
            # i think this part is the auto login
            #email = form.cleaned_data.get('email')
            #raw_password = form.cleaned_data.get('password1')
            #account = authenticate(email=email, password=raw_password)
            messages.success(request, 'Account was created for ' + user)
            #login(request, account)
            return redirect('verify_email')
        else:
            messages.error(request, 'Error processing your request')
            context = {'form': form}
            return render(request, 'register.html', context)

    return render(request, 'register.html', {})

def email_verify_code(request):
    if request.method == 'GET':
        form = VerifyEmailForm()
        context = {'form' : form}
        return render(request, 'verify_email.html', context)

    if request.method == 'POST':
        form = VerifyEmailForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                usr = Account.objects.get(uniqueId=code)
                messages.success(request, 'Email verified, please log in')
                usr.email_confirmed = True
                usr.save()
                return redirect('login')
            except:
                messages.error(request, 'Sorry, that code is incorrect.')
                context = {'form': form}
                return render(request, 'verify_email.html', context)
        else:
            messages.error(request, 'Error processing your request')
            context = {'form': form}
            return render(request, 'verify_email.html', context)

    return render(request, 'verify_email.html', {})


# New way to check if logged in (just on profile and home for now probably)
###########################
from django.contrib.auth.decorators import login_required, user_passes_test

def is_email_verified(user):
    return user.email_confirmed

#@login_required
#@user_passes_test(is_email_verified, 'verify_email', None)



##########################################
#NEW
############################################

# change public profile to generic except statement



@login_required
@user_passes_test(is_email_verified, 'verify_email', None)
def profile(request):
    # search
    job_search_form = SearchJobsForm()

    model = ProjectImplicit.objects.all()    

    context = {}
    context['job_search_form'] = job_search_form
    context['model'] = model    

    search_request = search(request)
    if search_request is not None:
        return search_request
    else:
        print("getting none")
    # end search

    usr = request.user

    context['object'] = request.user

    try:
        if usr.resume:
            educations = Education.objects.filter(resume=usr.resume)
            experiences = Experience.objects.filter(resume=usr.resume)
            context['educations'] = educations
            context['experiences'] = experiences

            if usr.resume.company:
                jobs = Job.objects.filter(company=usr.resume.company)
                context['postings'] = jobs             
    except:
        pass

    return render(request, 'profile.html', context)

@login_required
@user_passes_test(is_email_verified, 'verify_email', None)
def home_applicants(request):
    # search
    applicant_form = FilterApplicantsForm()
    applicant_list = Account.objects.filter(role='Applicant')

    context = {}
    context['applicant_form'] = applicant_form
    context['users'] = applicant_list

    if request.method == 'POST':
        applicant_form = FilterApplicantsForm(request.POST)
        context['applicant_form'] = applicant_form

        if applicant_form.is_valid():
            qualifications = applicant_form.cleaned_data.get('qualifications')
            location = applicant_form.cleaned_data.get('state')

            print(qualifications)

            quali_list = []
            loco_list = []

            if qualifications is not None and qualifications != []:
                quali_list = applicant_list.filter(resume__experience__skills__contains=qualifications)
                

            if location is not None and location != '' and location != 'N/A':
                # errors???
                loco_list = applicant_list.filter(resume__state=location)
            
            app_ls = []
            [app_ls.append(x) for x in quali_list if x not in app_ls]
            [app_ls.append(x) for x in loco_list if x not in app_ls]


            context['users'] = app_ls

            return render(request, 'home_applicants.html', context)

    return render(request, 'home_applicants.html', context)    






    if request.method == 'POST':
        job_search_form = SearchJobsForm(request.POST)
        context['job_search_form'] = job_search_form

        if job_search_form.is_valid():
            # might need to check if not None
            if filter and not job_filter_form.is_valid():
                messages.error(request, 'Error processing your request')
                context['job_search_form'] = job_search_form
                context['job_filter_form'] = job_filter_form
                return render(request, 'home.html', context)    

            search = job_search_form.cleaned_data.get('title')
            jobs = []
            if len(search.split()) > 1:
                search_list = search.split()
                item_list = []
                for item in search_list:
                    a_list = Job.objects.filter(title__icontains=item)
                    for x in a_list:
                            item_list.append(x)
                [jobs.append(x) for x in item_list if x not in jobs]

            else:
                jobs = Job.objects.filter(title__icontains=search)

            if filter:
                category = job_filter_form.cleaned_data.get('category')
                location = job_filter_form.cleaned_data.get('location')

                if category is not None and category != '' and category != 'N/A':
                    print('category' + category)
                    jobs = jobs.filter(category=category)
                if location is not None and location != '' and location != 'N/A':
                    print("location" + location)
                    jobs = jobs.filter(location=location)

            context['jobs'] = jobs
            context['title'] = search

            # only sending jobs that fit the search
            return render(request, 'home.html', context)
    
    return None





@login_required
@user_passes_test(is_email_verified, 'verify_email', None)
def home_employers(request):
	# search
	job_search_form = SearchJobsForm()

	context = {}
	context['job_search_form'] = job_search_form

	search_request = search(request)
	if search_request is not None:
		return search_request
	# end search

	#	can change to filter for search
	users_list = Account.objects.filter(role='Employer')
	context['users'] = users_list
	return render(request, 'home_employers.html', context)        


@login_required
@user_passes_test(is_email_verified, 'verify_email', None)
def create_resume(request, res_id=None):
    # search
    job_search_form = SearchJobsForm()

    context = {}
    context['job_search_form'] = job_search_form

    # applicants must verify their information
    if request.user.role == 'Applicant':
        need_conf = True
    else:
        need_conf = False

    if request.method == 'POST':
        search_request = search(request)

        if res_id:
            res = Resume.objects.get(pk=res_id)
            form = ResumeForm(request.POST, request.FILES, instance=res)
        else:
            # request.FILES bc files upload option in form
            form = ResumeForm(request.POST, request.FILES)

        if need_conf:
            conf_form = AnonForm(request.POST)

        if form.is_valid():

            if need_conf:
                if not conf_form.is_valid():
                    messages.error(request, 'Error processing your request')

                    context['form'] = form
                    context['conf_form'] = conf_form

                    return render(request, 'create-resume.html', context)

            obj = form.save(commit=False)
                

            # setting 1:1 attribute
            obj.user = request.user
            obj.last_updated = datetime.now

            obj.save()

            messages.success(request, 'Resume created successfully.')
            return redirect('profile')
        elif search_request is not None:
            return search_request
        else:
            messages.error(request, 'Error processing your request')
            context['form'] = form
            
            if need_conf:
                context['conf_form'] = conf_form
                return render(request, 'create-resume.html', context)
            else:
                return render(request, 'create-resume-employer.html', context)

    if request.method == 'GET':
        if res_id:
            res = Resume.objects.get(pk=res_id)
            form = ResumeForm(instance=res)
        else:
            form = ResumeForm()

        context['form'] = form

        if need_conf:
            conf_form = AnonForm(request.POST)
            context['conf_form'] = conf_form
            return render(request, 'create-resume.html', context)
        else:
            return render(request, 'create-resume-employer.html', context)

    if request.user.role == "Employer":
        return render(request, 'create-resume-employer.html', context)
    else:
        return render(request, 'create-resume.html', context)

from django.shortcuts import render

def BootstrapFilterView(request):
    qs = Job.object.all()
    categories = CreateJobForm.CAT_CHOICES
    locations = CreateJobForm.STATE_CHOICES

    category_query = request.GET.get('category')
    location_query = request.GET.get('location')
    print(category_query)
    print(location_query)

    if category_query != '' and category_query is not None and category_query != "Choose...":
        qs = qs.filter(category=category_query)
    # the way you do multiple is just continuing to do it to itself
    # i.e. qs = qs....
    if location_query != '' and location_query is not None and location_query != "default value":    
        qs=qs.filter(location=location_query)

    #qs = filter(request)
    context = {}
    context['queryset'] = qs
    context['categories'] = categories
    context['locations'] = locations

    return render(request, "bootstrap_form.html", context)

def search(request):
    job_search_form = SearchJobsForm()

    job_list = Job.objects.all()

    context = {}
    context['job_search_form'] = job_search_form
    context['jobs'] = job_list

    if filter:
        job_filter_form = FilterJobsForm()
        context['job_filter_form'] = job_filter_form

    if request.method == 'POST':
        job_search_form = SearchJobsForm(request.POST)
        context['job_search_form'] = job_search_form

        if filter:
            job_filter_form = FilterJobsForm(request.POST)
            context['job_filter_form'] = job_filter_form


        if job_search_form.is_valid():
            # might need to check if not None
            if filter and not job_filter_form.is_valid():
                messages.error(request, 'Error processing your request')
                context['job_search_form'] = job_search_form
                context['job_filter_form'] = job_filter_form
                return render(request, 'home.html', context)    

            search = job_search_form.cleaned_data.get('title')
            jobs = []
            if len(search.split()) > 1:
                search_list = search.split()
                item_list = []
                for item in search_list:
                    a_list = Job.objects.filter(title__icontains=item)
                    for x in a_list:
                            item_list.append(x)
                [jobs.append(x) for x in item_list if x not in jobs]

            else:
                jobs = Job.objects.filter(title__icontains=search)

            if filter:
                category = job_filter_form.cleaned_data.get('category')
                location = job_filter_form.cleaned_data.get('location')

                if category is not None and category != '' and category != 'N/A':
                    print('category' + category)
                    jobs = jobs.filter(category=category)
                if location is not None and location != '' and location != 'N/A':
                    print("location" + location)
                    jobs = jobs.filter(location=location)

            context['jobs'] = jobs
            context['title'] = search

            # only sending jobs that fit the search
            return render(request, 'home.html', context)
    
    return None


# no two forms
def search(request):
    job_search_form = SearchJobsForm()
    model = ProjectImplicit.objects.all()

    job_list = Job.objects.all()

    context = {}
    context['job_search_form'] = job_search_form
    context['jobs'] = job_list

    if request.method == 'POST':
        job_search_form = SearchJobsForm(request.POST)
        context['job_search_form'] = job_search_form

        if job_search_form.is_valid():
            # might need to check if not None  

            search = job_search_form.cleaned_data.get('title')
            jobs = []
            if len(search.split()) > 1:
                search_list = search.split()
                item_list = []
                for item in search_list:
                    a_list = Job.objects.filter(title__icontains=item)
                    for x in a_list:
                            item_list.append(x)
                [jobs.append(x) for x in item_list if x not in jobs]

            else:
                jobs = Job.objects.filter(title__icontains=search)

            category = job_search_form.cleaned_data.get('category')
            location = job_search_form.cleaned_data.get('location')

            if category is not None and category != '' and category != 'N/A':
                jobs = jobs.filter(category=category)
            if location is not None and location != '' and location != 'N/A':
                jobs = jobs.filter(state=location)

            context['jobs'] = jobs
            context['title'] = search

            # only sending jobs that fit the search
            return render(request, 'home.html', context)
    
    return None


@login_required()
def home(request):
	if not request.user.email_confirmed:
		return redirect('verify_email')
	# search
	job_search_form = SearchJobsForm()

	context = {}
	context['job_search_form'] = job_search_form

	search_request = search(request)
	if search_request is not None:
		return search_request
	# end search

	job_list = Job.objects.all()
	context['jobs'] = job_list

	return render(request, 'home.html', context)


# print out what those array fields look like
# iterate through them like you do with title
# maybe applicants dont need a title bc we didnt promise one
# search bar can be only for jobs and other "searches" can just be filter

