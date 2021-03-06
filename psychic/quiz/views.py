from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.utils import timezone

from .models import Quiz, Question, Choice, Prediction, Submission
from . import settings

import os
import pathlib


class IndexView(generic.ListView):
    template_name = 'quiz/index.html'
    context_object_name = 'quiz_list'

    def get_queryset(self):
        """
        Return all valid quizzes
        """
        return [quiz for quiz in Quiz.objects.all() if quiz.is_active() and quiz.is_valid()]


class QuizView(generic.DetailView):
    context_object_name = 'quiz'
    template_name = 'quiz/quiz.html'
    model = Quiz


def quiz(request, pk):
    selected_quiz = get_object_or_404(Quiz, pk=pk)
    if (selected_quiz.is_valid() and selected_quiz.is_active()) or settings.DEBUG:
        context = {
            'quiz': selected_quiz,
        }
        return render(request, 'quiz/quiz.html', context)
    else:
        return render(request, 'quiz/invalid.html')


def submit(request, quiz_id, question_format="question{}", save_path=settings.LOG_DIR):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz_results = {}

    time_submitted = timezone.now()
    quiz_results['time_submitted'] = time_submitted.isoformat()

    if 'name' in request.POST.keys() and request.POST['name']:
        quiz_results['name'] = request.POST['name']
    else:
        return HttpResponseBadRequest("No name provided!")

    if 'email' in request.POST.keys() and request.POST['email']:
        quiz_results['email'] = request.POST['email']
    else:
        return HttpResponseBadRequest("No email provided!")

    # Set up prediction set to sum relevant weights
    prediction_set = {}

    for prediction in quiz.prediction_set.all():
        prediction_set[prediction.pk] = 0

    # Set up selected choices set
    quiz_results['choices'] = {}

    for question in quiz.question_set.all():
        if not question_format.format(question.id) in request.POST.keys():
            return HttpResponseBadRequest("Please answer all of the questions")
        else:
            selected_choice = get_object_or_404(Choice, pk=request.POST[question_format.format(question.id)])
            selected_predictions = [i for i in [selected_choice.prediction, selected_choice.prediction2, selected_choice.prediction3, selected_choice.prediction4, selected_choice.prediction5] if i is not None]
            for prediction in selected_predictions:
                prediction_set[prediction.pk] += selected_choice.weight
            quiz_results['choices'][question.pk] = selected_choice.pk

    quiz_results['prediction_set'] = prediction_set

    final_prediction_pk = max(prediction_set.keys(), key=(lambda k: prediction_set[k]))
    final_prediction = Prediction.objects.get(pk=final_prediction_pk)

    quiz_results['prediction'] = final_prediction.prediction_title

    # Collect client data
    quiz_results['client_data'] = _get_client_data(request)

    # Write submission to database
    submission = Submission(quiz=quiz, client_name=quiz_results['name'],
                            client_email=quiz_results['email'], time_submitted=time_submitted,
                            calculated_prediction=final_prediction)
    submission.save()

    for choice_pk in quiz_results['choices'].values():
        submission.choices.add(Choice.objects.get(pk=choice_pk))

    return submit_response(request, quiz)


def submit_response(request, quiz):
    context = {
        'quiz': quiz,
    }
    return render(request, 'quiz/submit.html', context)


def _get_client_data(request):
    # Collect client data
    client_data = {
        'server_name': request.META['SERVER_NAME'],
        'server_port': request.META['SERVER_PORT'],
        'http_host': request.META['HTTP_HOST'],
        'http_user_agent': request.META['HTTP_USER_AGENT'],
        'clinet_ip': request.META['REMOTE_ADDR'],
    }

    return client_data

