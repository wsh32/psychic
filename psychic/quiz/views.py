import json

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from dicttoxml import dicttoxml

from .models import Quiz, Question, Choice


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

    for question in quiz.question_set.all():
        if not question_format.format(question.id) in request.POST.keys():
            # Throw error for unfinished quiz
            pass
        else:
            selected_choice = get_object_or_404(Choice, pk=request.POST[question_format.format(question.id)])
            quiz_results[question.question_text] = selected_choice.choice_text

    return HttpResponse(json.dumps(quiz_results))

