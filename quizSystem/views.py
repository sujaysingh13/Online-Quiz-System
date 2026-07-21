from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Test, Question, Result
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import random
from django.contrib.auth import update_session_auth_hash

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

@login_required
def dashboard(request):

    results = Result.objects.filter(
        student=request.user
    ).order_by("-attempted_on")

    return render(
        request,
        "quizSystem/dashboard.html",
        {
            "results": results
        }
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
            "You have already attempted this test. Only one attempt is allowed."
        )

        return redirect("tests")

    if request.method == "GET":

        questions = list(
            Question.objects.filter(test=test)
        )

        random.shuffle(questions)

        questions = questions[:test.number_of_questions]

        # Save question IDs in session
        request.session["question_ids"] = [
            question.id for question in questions
        ]

    if request.method == "POST":

        question_ids = request.session.get(
            "question_ids",
            []
        )

        questions = []

        for question_id in question_ids:
            questions.append(
                Question.objects.get(id=question_id)
            )

        score = 0
        correct_answers = 0

        for question in questions:

            selected_answer = request.POST.get(
                f"question_{question.id}"
            )

            if selected_answer == question.correct_answer:

                score += question.marks

                correct_answers += 1

        result = Result.objects.create(

            student=request.user,

            test=test,

            score=score,

            total_marks=test.total_marks,

            correct_answers=correct_answers

        )

        request.session.pop("question_ids", None)

        return redirect(
            "result_page",
            result_id=result.id
        )

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


@login_required
def profile(request):

    if request.method == "POST":

        fullname = request.POST.get("fullname", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()

        if not fullname:

            messages.error(
                request,
                "Full Name cannot be empty."
            )

            return redirect("profile")


        if not username:

            messages.error(
                request,
                "Username cannot be empty."
            )

            return redirect("profile")


        if not email:

            messages.error(
                request,
                "Email cannot be empty."
            )

            return redirect("profile")

        # Check if username already exists
        if User.objects.filter(username=username).exclude(id=request.user.id).exists():

            messages.error(
                request,
                "Username is already taken."
            )

            return redirect("profile")

        # Check if email already exists
        if User.objects.filter(email=email).exclude(id=request.user.id).exists():

            messages.error(
                request,
                "Email is already registered."
            )

            return redirect("profile")

        request.user.first_name = fullname
        request.user.username = username
        request.user.email = email

        request.user.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("profile")

    return render(
        request,
        "quizSystem/profile.html")


@login_required
def change_password(request):

    if request.method == "POST":

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if len(new_password) < 8:

            messages.error(
                request,
                "Password must be at least 8 characters long."
            )

            return redirect("change_password")


        if new_password == current_password:

            messages.error(
                request,
                "New password must be different from the current password."
            )

            return redirect("change_password")

        # Check current password
        if not request.user.check_password(current_password):

            messages.error(
                request,
                "Current password is incorrect."
            )

            return redirect("change_password")

        # Check both passwords match
        if new_password != confirm_password:

            messages.error(
                request,
                "New passwords do not match."
            )

            return redirect("change_password")

        # Update password
        request.user.set_password(new_password)

        request.user.save()

        # Keep the user logged in
        update_session_auth_hash(
            request,
            request.user
        )

        messages.success(
            request,
            "Password changed successfully."
        )

        return redirect("profile")

    return render(
        request,
        "quizSystem/change_password.html"
    )


@login_required
def result_page(request, result_id):

    result = get_object_or_404(
        Result,
        id=result_id,
        student=request.user
    )

    percentage = (
        result.score / result.total_marks
    ) * 100

    wrong_answers = (
        result.test.number_of_questions
        - result.correct_answers
    )

    if percentage >= 40:

        status = "PASS"

    else:

        status = "FAIL"

    return render(
        request,
        "quizSystem/result.html",
        {
            "result": result,
            "percentage": percentage,
            "wrong_answers": wrong_answers,
            "status": status
        }
    )