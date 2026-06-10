from django.shortcuts import render
from .models import User

# Create your views here.
def quizSystem_index(request):
    return render(request, 'quizSystem/index.html')

def user_signup(request):
    return render(request, 'quizSystem/signup.html')

def save_user(request):
    # receive all data
    fullname = request.POST.get('fullname')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')

    # send this data to database
    User.objects.create(fullname=fullname, email=email, username=username, password=password)

    return render(request, 'quizSystem/signup.html', {'message': "Registration Success"})