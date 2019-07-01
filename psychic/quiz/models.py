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


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


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

