from django.urls import re_path
from UserApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    re_path(r'^applicant$', views.applicantApi),
    re_path(r'applicant/([0-9]+)$', views.applicantApi),

    re_path(r'^employer$', views.employerApi),
    re_path(r'employer/([0-9]+)$', views.employerApi),

    re_path(r'^job_posting$', views.jobPostingApi),
    re_path(r'job_posting/([0-9]+)$', views.jobPostingApi),

    re_path(r'^applicant/save_file$', views.SaveFile),
    path('jobs/company/<slug:slug>', jobs_views.company_detail, name='company_detail'),
    path('all-companies/', users_views.home_companies, name='all_companies'),    



#########################
# NEW NOT YET IN VSERVER
#########################
    path('applicants/', users_views.home_applicants, name='app_users'),
    path('employers/', users_views.home_employers, name='emp_users'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

