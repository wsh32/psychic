import json

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from dicttoxml import dicttoxml

from .models import Quiz, Question, Choice, Prediction


class IndexView(generic.ListView):
    template_name = 'quiz/index.html'
    context_object_name = 'quiz_list'

    def get_queryset(self):
        """
        Return all valid quizzes
        """
        return [quiz for quiz in Quiz.objects.all() if quiz.is_active()]


class QuizView(generic.DetailView):
    context_object_name = 'quiz'
    template_name = 'quiz/quiz.html'
    model = Quiz


class QuestionView(generic.DetailView):
    context_object_name = 'question'
    template_name = 'quiz/question.html'
    model = Question


def submit(request, quiz_id, question_format="question{}"):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz_results = {}

    if 'name' in request.POST.keys():
        quiz_results['name'] = request.POST['name']

    if 'email' in request.POST.keys():
        quiz_results['email'] = request.POST['email']

    prediction_set = {}

    for prediction in Prediction.objects.filter(quiz=quiz):
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
    client_data = {
        'server_name': request.META['SERVER_NAME'],
        'server_port': request.META['SERVER_PORT'],
        'http_host': request.META['HTTP_HOST'],
        'http_user_agent': request.META['HTTP_USER_AGENT'],
        'clinet_ip': request.META['REMOTE_ADDR'],
    }

    quiz_results['client_data'] = client_data

    return HttpResponse(json.dumps(quiz_results))

