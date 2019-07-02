import datetime

from django.db import models
from django.utils import timezone


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('publish_date')
    exp_date = models.DateTimeField('expire_date')

    def __str__(self):
        return self.title

    def is_active(self, time_to_check=timezone.now()):
        return time_to_check >= self.pub_date and time_to_check <= self.exp_date

    def is_valid(self):
        if not self.question_set.all():
            return False
        for question in self.question_set.all():
            if not question.is_valid():
                return False
        return True


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

    def is_valid(self):
        """
        Criteria for a valid question: must have 2+ choices, must have only valid choices
        """
        if not self.choice_set.all() and len(self.choice_set.all()) >= 2:
            return False
        for choice in self.choice_set.all():
            if not choice.is_valid():
                return False
        return True


class Prediction(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    prediction_title = models.CharField(max_length=200)

    def __str__(self):
        return self.prediction_title


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    prediction = models.ForeignKey(Prediction, on_delete=models.SET_NULL, null=True)
    weight = models.FloatField()

    def __str__(self):
        return self.choice_text

    def is_valid(self):
        """
        Criteria for a valid choice: prediction and question must be of the same quiz
        """
        if self.prediction.quiz.pk != self.question.quiz.pk:
            return False
        return True

class Submission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=200)
    client_email = models.CharField(max_length=200)
    time_submitted = models.DateTimeField('time_submitted')
    calculated_prediction = models.ForeignKey(Prediction, on_delete=models.SET_NULL, null=True)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return self.client_name.replace(" ", "")

