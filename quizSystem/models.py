from django.db import models

# Create your models here.
from django.db import models

class Test(models.Model):

    subject = models.CharField(max_length=100)

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    duration = models.IntegerField(help_text="Duration in minutes")

    total_marks = models.IntegerField(default=15)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    

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
        return self.question