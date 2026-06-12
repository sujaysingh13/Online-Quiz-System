from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

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

def logout_user(request):

    request.session.flush()

    return redirect('quizSystem_index')

def user_signup(request):
    return render(request, 'quizSystem/signup.html')

def user_login(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(
                username=username,
                password=password
            )

            request.session['username'] = user.username
            request.session['fullname'] = user.fullname

            return redirect('quizSystem_index')

        except User.DoesNotExist:
            messages.error(request, "Invalid username or password")

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