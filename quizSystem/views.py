from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def quizSystem_index(request):
    return render(request, 'quizSystem/index.html')

def user_signup(request):
    return render(request, 'quizSystem/signup.html')

def user_login(request):
    return render(request, 'quizSystem/login.html')

def dashboard(request):
    return render(request, 'quizSystem/dashboard.html')

def quiz_page(request):
    return render(request, 'quizSystem/quiz.html')

def digital_logic(request):
    return render(request, 'quizSystem/digital_logic.html')

def operating_system(request):
    return render(request, 'quizSystem/operating_system.html')

def dbms(request):
    return render(request, 'quizSystem/dbms.html')

def save_user(request):
    if request.method == "POST":

        # receive all data
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # send this data to database
        User.objects.create(fullname=fullname, email=email, username=username, password=password)

        messages.success(request, "Your account has been created successfully!")

        return redirect('user_login')

    return render(request, 'quizSystem/signup.html')