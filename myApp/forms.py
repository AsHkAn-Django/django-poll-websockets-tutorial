from django import forms
from .models import Poll, Question, Answer
from django.forms import modelformset_factory, inlineformset_factory


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('body',)
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('body',)
        
class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('title',)
        


QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=3, can_delete=False)
        
AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=2, can_delete=False)

class PollSubmissionForm(forms.Form):
    def __init__(self, *args, poll=None, **kwargs):
        super().__init__(*args, **kwargs)
        if poll:
            for question in poll.questions.all():
                choices = [(answer.id, answer.body) for answer in question.answers.all()]
                self.fields[f"question_{question.id}"] = forms.ChoiceField(
                    label=question.body,
                    choices=choices,
                    widget=forms.RadioSelect,
                    required=True
                )
    
        

