from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Test, Question, Result
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import random

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

    all_tests = Test.objects.filter(is_active=True)

    now = timezone.now()

    for test in all_tests:

        if now < test.start_time:
            test.status = "Not Started"

        elif now > test.end_time:
            test.status = "Expired"

        else:
            test.status = "Available"

    return render(
        request,
        "quizSystem/tests.html",
        {
            "tests": all_tests
        }
    )


@login_required
def start_test(request, test_id):

    test = get_object_or_404(Test, id=test_id)

    already_attempted = Result.objects.filter(
        student=request.user,
        test=test
    ).exists()

    if already_attempted:

        messages.error(
            request,
            "You have already attempted this test."
        )

        return redirect("tests")

    questions = list(
        Question.objects.filter(test=test)
    )

    random.shuffle(questions)

    questions = questions[:test.number_of_questions]

    if request.method == "POST":

        score = 0
        correct_answers = 0

        for question in questions:

            selected_answer = request.POST.get(
                f"question_{question.id}"
            )

            if selected_answer == question.correct_answer:

                score += question.marks

                correct_answers += 1

        print("Score:", score)

        print("Correct:", correct_answers)

    return render(
        request,
        "quizSystem/quiz.html",
        {
            "test": test,
            "questions": questions
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