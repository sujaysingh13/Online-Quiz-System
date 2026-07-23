from django.shortcuts import render

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from quizSystem.models import Test, Question, Result


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def admin_app_index(request):

    total_students = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).count()

    total_tests = Test.objects.count()

    total_questions = Question.objects.count()

    total_attempts = Result.objects.count()

    context = {

        "total_students": total_students,

        "total_tests": total_tests,

        "total_questions": total_questions,

        "total_attempts": total_attempts,

    }

    return render(
        request,
        "admin_app/index.html",
        context
    )