from django.shortcuts import render
# Allow other domains to access API methods
from django.views.decorators.csrf import csrf_exempt
# Parse incoming data into datamodel
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from TestApp.models import Departments, Employees
from TestApp.serializers import DepartmentSerializer, EmployeeSerializer

from django.core.files.storage import default_storage

# Create your views here.

@csrf_exempt
def departmentApi(request, id=0):
    if request.method == 'GET':
        departments = Departments.objects.all()
        departments_serializer = DepartmentSerializer(departments, many=True)
        return JsonResponse(departments_serializer.data, safe=False)
    elif request.method == 'POST':
        department_data = JSONParser().parse(request)
        departments_serializer = DepartmentSerializer(data=department_data)
        if departments_serializer.is_valid():
            departments_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        department_data = JSONParser().parse(request)
        department = Departments.objects.get(DepartmentId = department_data['DepartmentId'])
        departments_serializer = DepartmentSerializer(department, data = department_data)
        if departments_serializer.is_valid():
            departments_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        department = Departments.objects.get(DepartmentId = id)
        department.delete()
        return JsonResponse("Deleted Success", safe=False)

@csrf_exempt
def employeeApi(request, id=0):
    if request.method == 'GET':
        employees = Employees.objects.all()
        employees_serializer = EmployeeSerializer(employees, many=True)
        return JsonResponse(employees_serializer.data, safe=False)
    elif request.method == 'POST':
        employee_data = JSONParser().parse(request)
        employees_serializer = EmployeeSerializer(data=employee_data)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        employee_data = JSONParser().parse(request)
        employee = Employees.objects.get(EmployeeId = employee_data['EmployeeId'])
        employees_serializer = EmployeeSerializer(employee, data = employee_data)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        employee = Employees.objects.get(EmployeeId = id)
        employee.delete()
        return JsonResponse("Deleted Success", safe=False)

@csrf_exempt
def SaveFile(request):
    file = request.FILES['file']
    file_name = default_storage.save(file.name, file)
    return JsonResponse(file_name, safe=False)

def sendEmail(emailAddr, emailDetails, subject):
    from_email = settings.EMAIL_HOST_USER
    to_email = emailAddr
    text_content = """
             {}
             {}
             {}
             {}          
             Best,
                  The LinkedIncognito Team
                                                     
                     """.format(emailDetails['title'], emailDetails['subtitle'], emailDetails['message'], emailDetails['link'])
    
    html_c = get_template('email.html')
    d = {'email': email}
    html_content = html_c.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def sendInvitation(invitee, employer, response):
    content = {}
    content['title'] = 'Hey There!'
    content['subtitle'] = 'You have been invited to an interview with ' + employer + '.'
    content['message'] = 'Here is the link to join your meeting ' + \
        response['join_url'] + ' at ' + response['start_time'] + '. If this time does not work for you, click the button below to notify your employer.'
    content['link'] = 'http://159.203.182.153:8000/sendRejection'

    subject = 'Interview Scheduled'
    sendEmail(invitee, content, "Interview Invitation")
    

def sendConfirmation(receiver, response):
    content = {}
    content['title'] = 'Hey There!'
    content['subtitle'] = 'You have successfully scheduled your interview.'
    content['message'] = 'Here is the link to start your meeting ' + \
        response['start_url'] + ' at ' + response['start_time']
    content['link'] = 'http://159.203.182.153:8000/'

    sendEmail(receiver, content, "Interview Scheduled")

@csrf_protect
def sendRejection(request):
    if request.method == "POST":

        receiver = Accounts.objects.get(username=request.POST["employer"]) 

        content = {}
        content['title'] = 'Hey There!'
        content['subtitle'] = request.user.username + ' has rejected your interview invitation.'
        content['message'] = 'Here is the link to schedule a new meeting:'
        content['link'] = 'http://159.203.182.153:8000/meetingCreation'

        sendEmail(receiver.email, content, "Interview Rejected")

@csrf_protect
def createMeeting(request):
    if request.method == "POST":

        meetingdetails = {"topic": request.POST["topic"],
                          "type": 2,

                          "start_time": request.POST["time"],
                          "duration": request.POST["duration"],
                          "timezone": "Eastern Time",
                          "agenda": "LinkedIncognito Interview",
                          "settings": {"host_video": "true",
                                       "participant_video": "False",
                                       "join_before_host": "False",
                                       "mute_upon_entry": "False",
                                       "watermark": "true",
                                       "audio": "voip",
                                       "meeting_authentication": "False"
                                       }
                          }
        headers = {'authorization': 'Bearer %s' % generateToken(),
                   'content-type': 'application/json'}

        r = requests.post(
            f'https://api.zoom.us/v2/users/me/meetings', headers=headers, data=json.dumps(meetingdetails))


        invitee = Accounts.objects.get(username=request.POST["invitee"])     

        sendInvitation(invitee.email, request.user.first_name, r.json())
        sendConfirmation(request.user.email,r.json())

        return render(request, "meetingCreation.html", r.json())
    else:
        return render(request, "meetingCreation.html")
