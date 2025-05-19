from django import forms
from .models import Poll, Question, Answer, Response


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('body','poll',)
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('body', 'question',)
        
class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('title',)
        

