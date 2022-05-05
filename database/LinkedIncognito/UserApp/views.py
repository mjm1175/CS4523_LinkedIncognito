from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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
from .forms import RegisterForm

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
def create_resume(request):
    if request.method == 'POST':
        # request.FILES bc files upload option in form
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)

            # setting 1:1 attribute
            obj.user = request.user
            request.user.company = form.company

            obj.save()

            messages.success(request, 'Resume created successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Error processing your request')
            context = {'form': form}
            return render(request, 'create-resume.html', context)

    if request.method == 'GET':
        form = ResumeForm()
        context = {'form': form}
        return render(request, 'create-resume.html', context)

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
