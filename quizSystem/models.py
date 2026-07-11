# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Test(models.Model):

    title = models.CharField(max_length=200)

    subject = models.CharField(max_length=100)

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    duration = models.IntegerField(help_text="Duration in minutes")

    number_of_questions = models.IntegerField(default=15)

    total_marks = models.IntegerField(default=15)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError(
                "End time must be after start time."
            )

    def __str__(self):
        return f"{self.title} ({self.subject})"
    

class Question(models.Model):

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question = models.TextField()

    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)

    ANSWER_CHOICES = [
        ("option1", "Option 1"),
        ("option2", "Option 2"),
        ("option3", "Option 3"),
        ("option4", "Option 4"),
    ]

    correct_answer = models.CharField(
        max_length=10,
        choices=ANSWER_CHOICES
    )

    marks = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.test.title} - {self.question[:50]}"
    

class Result(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE
    )

    score = models.IntegerField()

    total_marks = models.IntegerField()

    correct_answers = models.IntegerField()

    attempted_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.username} - {self.test.title}"