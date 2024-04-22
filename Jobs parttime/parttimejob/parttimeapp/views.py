from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import UserProfile,Job,Applicant
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from joblib.applylib import print_apply
import boto3
from django.views.decorators.csrf import csrf_exempt




# Create your views here.
def home(request):
    posts = Job.objects.all()
    regtype = None
    
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            regtype = profile.regtype
        except UserProfile.DoesNotExist:
            pass

    context = {'posts': posts, 'regtype': regtype}  # Fixed the variable name 'posts' and corrected the syntax
    return render(request, 'home.html', context)

# 'posts': posts, 

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        phonenumber = request.POST['phoneno']
        regtype = request.POST['regtype']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname 
        myuser.save()
        
        
        profile = UserProfile.objects.create(user=myuser, regtype=regtype)

        messages.success(request, "You have Successfully Signed up")
        return redirect("login")
    
    return render(request, "signup.html")

@csrf_exempt
def logoutpage(request):       
    logout(request)
    return redirect('home')
@csrf_exempt
def addjob(request):
    if request.method == "POST":
        user = request.user
        title = request.POST['title']
        description = request.POST['description']
        requirements = request.POST['requirements']
        salary = request.POST['salary']
        address = request.POST['address']
        contact_information = request.POST['contact_information']
        
        job_id = get_random_string(length=8)
        
        new_job = Job.objects.create(
            user=user,
            job_id=job_id,
            title=title,
            description=description,
            requirements=requirements,
            salary=salary,
            address=address,
            contact_information=contact_information
        )
        return redirect('home')

    return render(request, "addjob.html")

def dashboard(request):
    bookings = Applicant.objects.filter(user=request.user).select_related('job')
    status = print_apply()  
    context = {'bookings': bookings, 'status': status}  
    return render(request, 'dashboard.html', context)

@csrf_exempt
def applyjob(request, job_id):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        resume = request.FILES.get('resume')

        try:
            job = Job.objects.get(id=job_id)
            new_applicant = Applicant.objects.create(
                user=user,
                job=job,
                name=name,
                email=email,
                phone=phone,
                resume=resume,
            )

            # Send SNS notification
            # topicOfArn = 'arn:aws:sns:eu-west-1:250738637992:JobAlerts'
            
           
            subjectToSend = 'Job Application Received'
            messageToSend = f'A new application has been received for the job: {job.title}'
            AWS_REGION = 'eu-west-1'
            sns_client = boto3.client('sns', region_name=AWS_REGION)
            response = sns_client.publish(
                TopicArn=topicOfArn,
                Message=messageToSend,
                Subject=subjectToSend,
            )
            print(response)

            messages.success(request, "Application submitted successfully.")
            return redirect('home')
        except ObjectDoesNotExist:
            messages.error(request, "The job you are applying for does not exist.")
            return redirect('home')
        except Exception as e:
            messages.error(request, "An error occurred while sending the SNS notification.")
            print("SNS Error:", e)
            return redirect('home')

    else:
        # Pass the job_id to the template context
        context = {'job_id': job_id}
        return render(request, 'apply.html', context)

@csrf_exempt    
def update_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        job.title = request.POST['title']
        job.description = request.POST['description']
        job.requirements = request.POST['requirements']
        job.salary = request.POST['salary']
        job.address = request.POST['address']
        job.contact_information = request.POST['contact_information']

        job.save()

        return redirect('home')  # Redirect to the appropriate page after updating the job

    context = {'job': job}
    return render(request, 'update.html', context)
@csrf_exempt
def delete_job(request, job_id):
  booking = Job.objects.get(id=job_id, user=request.user)
  booking.delete()
  return redirect('home')
  
 