from django.shortcuts import render
from django.views import generic
from .models import Question



class QuestionListView(generic.ListView):
    model = Question
    template_name = "myApp/index.html"
    context_object_name = 'questions'

