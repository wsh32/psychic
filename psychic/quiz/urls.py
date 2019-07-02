from django.urls import path

from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.quiz, name='quiz'),
    path('<int:quiz_id>/submit', views.submit, name='submit'),
]
