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
        Return the last 5 valid published quizzes
        """
        return Quiz.objects.order_by('-pub_date')[:5]


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
    for question in quiz.question_set.all():
        if not question_format.format(question.id) in request.POST.keys():
            # Throw error for unfinished quiz
            pass
        else:
            selected_choice = get_object_or_404(Choice, pk=request.POST[question_format.format(question.id)])
            quiz_results[question.question_text] = selected_choice.choice_text
    return HttpResponse(json.dumps(quiz_results))

