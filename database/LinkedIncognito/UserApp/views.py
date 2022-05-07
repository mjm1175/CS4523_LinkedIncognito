from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pytz import timezone
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from UserApp.models import Applicants, Employers, JobPosting
from UserApp.serializers import ApplicantSerializer, EmployerSerializer, JobPostingSerializer

from django.core.files.storage import default_storage
# Create your views here.

###################################### Applicant API #######################################
@csrf_exempt
def applicantApi(request, id=0):
    if request.method=='GET':
        applicants = Applicants.objects.all()
        applicants_serializer = ApplicantSerializer(applicants, many=True)
        return JsonResponse(applicants_serializer.data, safe=False)
    elif request.method=='POST':
        applicant_data = JSONParser().parse(request)
        applicants_serializer = ApplicantSerializer(data=applicant_data)
        if applicants_serializer.is_valid():
            applicants_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method=='PUT':
        applicant_data = JSONParser().parse(request)
        applicant = Applicants.objects.get(Username=applicant_data['Username'])
        applicants_serializer = ApplicantSerializer(applicant, data=applicant_data)
        if applicants_serializer.is_valid():
            applicants_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method=='DELETE':
        applicant = Applicants.objects.get(Username=id)
        applicant.delete()
        return JsonResponse("Deleted Successfully", safe=False)

###################################### Employer API #######################################
@csrf_exempt
def employerApi(request, id=0):
    if request.method=='GET':
        employers = Employers.objects.all()
        employers_serializer = EmployerSerializer(employers, many=True)
        return JsonResponse(employers_serializer.data, safe=False)
    elif request.method=='POST':
        employer_data = JSONParser().parse(request)
        employers_serializer = EmployerSerializer(data=employer_data)
        if employers_serializer.is_valid():
            employers_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method=='PUT':
        employer_data = JSONParser().parse(request)
        employer = Employers.objects.get(Username=employer_data['Username'])
        employers_serializer = EmployerSerializer(employer, data=employer_data)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method=='DELETE':
        employer = Employer.objects.get(Username=id)
        employer.delete()
        return JsonResponse("Deleted Successfully", safe=False)

###################################### JobPosting API #######################################
@csrf_exempt
def jobPostingApi(request, id=0):
    if request.method=='GET':
        jobs = JobPosting.objects.all()
        jobs_serializer = JobPostingSerializer(jobs, many=True)
        return JsonResponse(jobs_serializer.data, safe=False)
    elif request.method=='POST':
        job_data = JSONParser().parse(request)
        jobs_serializer = JobPostingSerializer(data=job_data)
        if jobs_serializer.is_valid():
            jobs_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method=='PUT':
        job_data = JSONParser().parse(request)
        job = JobPosting.objects.get(Title=job_data['Title'])
        jobs_serializer = JobPostingSerializer(job, data=job_data)
        if jobs_serializer.is_valid():
            jobs_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method=='DELETE':
        job = JobPosting.objects.get(Title=id)
        job.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def SaveFile(request):
        file=request.FILES['file']
        file_name=default_storage.save(file.name, file)
        return JsonResponse(file_name, safe=False)


from django.contrib.auth import login, authenticate
from .forms import ApplicationForm, CreateCompanyForm, RegisterForm, ResumeForm, SearchJobsForm

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



@login_required
def create_resume(request, res_id=None):
    if request.method == 'POST':
        if res_id:
            res = Resume.objects.get(pk=res_id)
            form = ResumeForm(request.POST, request.FILES, instance=res)
        else:
            # request.FILES bc files upload option in form
            form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)

            # setting 1:1 attribute
            obj.user = request.user

            obj.save()

            messages.success(request, 'Resume created successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Error processing your request')
            context = {'form': form}
            if request.user.role == "Employer":
                return render(request, 'create-resume-employer.html', context)
            else:
                return render(request, 'create-resume.html', context)

    if request.method == 'GET':
        if res_id:
            res = Resume.objects.get(pk=res_id)
            form = ResumeForm(instance=res)
        else:
            form = ResumeForm()
        context = {'form': form}
        if request.user.role == "Employer":
            return render(request, 'create-resume-employer.html', context)
        else:
            return render(request, 'create-resume.html', context)

    if request.user.role == "Employer":
        return render(request, 'create-resume-employer.html', {})
    else:
        return render(request, 'create-resume.html', {})


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



# home page; primative search
@login_required
def home(request):
    form = SearchJobsForm()

    job_list = Job.objects.all()

    context = {}
    context['form'] = form
    context['jobs'] = job_list

    if request.method == 'POST':
        form = SearchJobsForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('title')
            jobs = Job.objects.filter(title__icontains=search)

            context['jobs'] = jobs
            context['title'] = search

            # only sending jobs that fit the search
            return render(request, 'home.html', context)
    
        else:
            messages.error(request, 'Error processing your request')
            context['form'] = form
            return render(request, 'home.html', context)
    
    return render(request, 'home.html', context)

# home page; smart search
@login_required
def home(request):
    job_search_form = SearchJobsForm()

    job_list = Job.objects.all()

    context = {}
    context['form'] = job_search_form
    context['jobs'] = job_list

    if request.method == 'POST':
        job_search_form = SearchJobsForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('title')
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
            context['form'] = job_search_form
            return render(request, 'home.html', context)
    
    return render(request, 'home.html', context)


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