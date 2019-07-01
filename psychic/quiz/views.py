import json

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, Http404
from django.utils import timezone
from dicttoxml import dicttoxml

from .models import Quiz, Question, Choice, Prediction
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
        raise Http404("Quiz does not exist!")


def submit(request, quiz_id, question_format="question{}", save_path=settings.LOG_DIR):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz_results = {}

    quiz_results['time_submitted'] = timezone.now().isoformat()

    if 'name' in request.POST.keys():
        quiz_results['name'] = request.POST['name']
    else:
        # TODO throw error for unfinished quiz
        pass

    if 'email' in request.POST.keys():
        quiz_results['email'] = request.POST['email']
    else:
        # TODO throw error for unfinished quiz
        pass

    prediction_set = {}

    for prediction in quiz.prediction_set.all():
        prediction_set[prediction.pk] = 0

    for question in quiz.question_set.all():
        if not question_format.format(question.id) in request.POST.keys():
            # Throw error for unfinished quiz
            pass
        else:
            selected_choice = get_object_or_404(Choice, pk=request.POST[question_format.format(question.id)])
            selected_prediction = selected_choice.prediction
            prediction_set[selected_prediction.pk] += selected_choice.weight
            quiz_results[question.question_text] = selected_choice.choice_text

    quiz_results['prediction_set'] = prediction_set

    final_prediction_pk = max(prediction_set.keys(), key=(lambda k: prediction_set[k]))
    final_prediction = Prediction.objects.get(pk=final_prediction_pk)

    quiz_results['prediction'] = final_prediction.prediction_title

    # Collect client data
    quiz_results['client_data'] = _get_client_data()

    # Save data
    log_subdir = str(quiz.pk)
    filename = "{}.json".format(request.POST['name'].replace(" ", ""))
    _log_json(save_path, log_subdir, filename)

    return HttpResponse(json.dumps(quiz_results))


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


def _log_json(save_path, log_subdir, filename):
    # Save data
    logdir = os.path.join(save_path, log_subdir)
    if not os.path.exists(save_path):
        pathlib.Path(logdir).mkdir(parents=True, exist_ok=True)

    # Write data
    with open(os.path.join(logdir, filename), 'w') as outfile:
        json.dump(quiz_results, outfile)

