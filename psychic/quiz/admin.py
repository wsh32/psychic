from django.contrib import admin

from .models import Quiz, Question, Choice, Prediction, Submission


class PredictionInLine(admin.TabularInline):
    model = Prediction
    fields = ['prediction_title']
    extra = 4


class ChoiceInLine(admin.TabularInline):
    model = Choice
    fields = ['choice_text', 'question', 'prediction', 'weight']
    extra = 4


class QuestionInLine(admin.TabularInline):
    model = Question
    fields = ['question_text']
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fields = ['quiz', 'question_text']
    inlines = [ChoiceInLine]


class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'submit_text']}),
        ('Date Information', {'fields': ['pub_date', 'exp_date'], 'classes': ['collapse']}),
    ]
    inlines = [PredictionInLine, QuestionInLine]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission)

