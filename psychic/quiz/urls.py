from django.urls import path

from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.QuestionView.as_view(), name='question'),
    path('<int:question_id>/submit', views.submit, name='submit'),
    path('quiz/<int:question_id>/', views.question, name='quiz'),
]
