from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Announcement, Application,Payroll
from django.contrib.auth.models import User
from django.contrib import messages

@login_required 
def home_employee(request):
    announcements = Announcement.objects.all()
    applications = Application.objects.all()
    if request.user.is_staff:
        payrolls = Payroll.objects.all()
    else:
        payrolls = Payroll.objects.filter(employee=request.user)
    return render(request,"home.html",context={'announcements':announcements, 'applications': applications,'payrolls':payrolls})

def announcement_list(request):
    announcements = Announcement.objects.order_by('-created_at')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            Announcement.objects.create(title=title, content=content)
            return redirect('Employee:announcement_list')

    return render(request, 'announcement_list.html', {
        'announcements': announcements
    })


def apply_work(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        reason = request.POST.get('reason')
        skills = request.POST.get('skills')

    
        Application.objects.create(
            name=name,
            age=age,
            reason=reason,
            skills=skills,
            user=request.user 
        )
        return redirect('Employee:application')  
    return render(request, 'apply_work.html')


def application(request):
    applications = Application.objects.all()
    return render(request, 'application_list.html', {'applications': applications})


def update_application(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':
        application.name = request.POST.get('name')
        application.age = request.POST.get('age')
        application.experience = request.POST.get('experience')
        application.skills = request.POST.get('skills')
        application.cover_letter = request.POST.get('why_us')
        application.save()
        return redirect('Employee:application')  

    return render(request, 'update_application.html', {'application': application})


def update_status(request, pk, new_status):
    if request.user.is_superuser or request.user.is_staff:
        application = get_object_or_404(Application, pk=pk)
        if new_status in ['Accepted', 'Rejected']:
            application.status = new_status
            application.save()
    return redirect('Employee:application') 

@login_required
def clear_requests(request):
    if request.method == "POST":
        Application.objects.all().delete()
    return redirect('Employee:application') 

@login_required
def clear_request(request):
    if request.method == "POST":
        Announcement.objects.all().delete()
    return redirect('Employee:announcement_list') 


@login_required
def payroll(request):
   
    if request.user.is_staff:
        payrolls = Payroll.objects.all()
    else:
        payrolls = Payroll.objects.filter(employee=request.user)
    
   
    context = {
        'payrolls': payrolls,
    }
    
    return render(request, 'payroll.html', context) 


@login_required
def payroll_list(request):
    if request.user.is_staff:
        payrolls = Payroll.objects.all()
    else:
        payrolls = Payroll.objects.filter(employee=request.user)

    context = {
        'payrolls': payrolls,
    }
    
    return render(request, 'payroll_list.html', context)


def add_payroll(request):
    users = User.objects.all() 

    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        salary = request.POST.get('salary')
        deductions = request.POST.get('deductions')
        month = request.POST.get('month')

        employee = User.objects.get(id=employee_id)

        Payroll.objects.create(
            employee=employee,
            salary=salary,
            deductions=deductions,
            month=month
        )

        return redirect('Employee:payroll_list')

    return render(request, 'add_payroll.html', {'users': users})



#-------------------------------------------------------------------------------------------------------


# @login_required
# def create_performance_evaluation(request):
#     if not request.user.is_staff:
#         return redirect('home')  # Only staff can evaluate

#     if request.method == 'POST':
#         # Extracting the data from the POST request
#         employee_id = request.POST.get('employee')
#         month = request.POST.get('month')
#         communication_score = request.POST.get('communication_score')
#         punctuality_score = request.POST.get('punctuality_score')
#         task_completion_score = request.POST.get('task_completion_score')
#         comments = request.POST.get('comments')

#         # Get the employee and manager (logged in user) from the database
#         employee = User.objects.get(id=employee_id)
#         manager = request.user

#         # Create the PerformanceEvaluation object and save it to the database
#         evaluation = PerformanceEvaluation(
#             employee=employee,
#             manager=manager,
#             month=month,
#             communication_score=communication_score,
#             punctuality_score=punctuality_score,
#             task_completion_score=task_completion_score,
#             comments=comments
#         )
#         evaluation.save()

#         messages.success(request, "Performance evaluation created successfully.")
#         return redirect('Employee:performance_list')  # Redirect to the performance list page
#     else:
#         # GET request, just render the form template
#         return render(request, 'create_performance_evaluation.html')

# # View to display performance evaluations for the logged-in employee
# @login_required
# def performance_list(request):
#     evaluations = PerformanceEvaluation.objects.filter(employee=request.user)
#     return render(request, 'performance_list.html', {'evaluations': evaluations})

# # Admin or manager view to see all evaluations for employees
# @login_required
# def performance_dashboard(request):
#     if not request.user.is_staff:
#         return redirect('home')  # Only staff can access this page

#     evaluations = PerformanceEvaluation.objects.all()
#     return render(request, 'performance_dashboard.html', {'evaluations': evaluations})