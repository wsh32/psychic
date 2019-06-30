from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from dicttoxml import dicttoxml

from .models import Question


class IndexView(generic.ListView):
    template_name = 'quiz/index.html'
    context_object_name = 'quiz_list'

    def get_queryset(self):
        """
        Return the last 5 valid published quizzes
        """
        return Question.objects.order_by('-pub_date')[:5]

def index(request):
    # TODO load list template
    return HttpResponse("Hello World!")

class QuestionView(generic.DetailView):
    template_name = 'quiz/question.html'
    model = Question

def question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    context = {
        'question': question,
    }

    return render(request, 'quiz/question.html', context)

def submit(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = question.choice_set.get(pk=request.POST['choice'])
        choice_text = choice.choice_text
    except (KeyError, Choice.DoesNotExist):
        choice_text = "Error 404"
    return_data = {
        'question_text': question.question_text,
        'choice': choice_text,
    }
    xml_response = dicttoxml(return_data)
    return HttpResponse(xml_response, content_type='application/xml')

