from django.shortcuts import render

# Create your views here.
def quizSystem_index(request):
    return render(request, 'quizSystem/index.html')

def user_signup(request):
    return render(request, 'quizSystem/signup.html')

