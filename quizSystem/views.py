from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Test
from django.contrib.auth.decorators import login_required

# Create your views here.
def quizSystem_index(request):
    fullname = request.session.get('fullname')

    return render(
        request,
        'quizSystem/index.html',
        {
            'fullname': fullname
        }
    )

def user_signup(request):
    return render(request, 'quizSystem/signup.html')

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('quizSystem_index')

        messages.error(request, "Invalid username or password")

    return render(request, 'quizSystem/login.html')


def logout_user(request):
    logout(request)
    return redirect('quizSystem_index')


def dashboard(request):

    tests = [
        {
            "test_no": 1,
            "subject": "Digital Logic",
            "date": "12-06-2026",
            "time": "10:30 AM",
            "score": 12
        },
        {
            "test_no": 2,
            "subject": "Operating System",
            "date": "12-06-2026",
            "time": "11:45 AM",
            "score": 14
        },
        {
            "test_no": 3,
            "subject": "DBMS",
            "date": "12-06-2026",
            "time": "02:15 PM",
            "score": 13
        }
    ]

    return render(
        request,
        'quizSystem/dashboard.html',
        {'tests': tests}
    )

@login_required
def tests(request):

    tests = Test.objects.filter(is_active=True)

    return render(
        request,
        'quizSystem/tests.html',
        {
            'tests': tests
        }
    )

def quiz_page(request):
    return render(request, 'quizSystem/quiz.html')

def save_user(request):

    if request.method == "POST":

        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('user_signup')

        User.objects.create_user(
            first_name=fullname,
            email=email,
            username=username,
            password=password
        )

        messages.success(request, "Your account has been created successfully!")

        return redirect('user_login')

    return render(request, 'quizSystem/signup.html')