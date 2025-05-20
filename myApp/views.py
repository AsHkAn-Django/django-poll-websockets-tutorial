from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Question, Poll, Submission, Answer, SubmittedAnswer
from .forms import PollSubmissionForm , PollForm, QuestionForm, AnswerForm, QuestionFormSet
from django.contrib.auth.decorators import login_required



class PollListView(generic.ListView):
    model = Poll
    template_name = "myApp/index.html"
    context_object_name = 'polls'
    


@login_required
def poll_view(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.method == "POST":
        form = PollSubmissionForm(request.POST, poll=poll)
        if form.is_valid():
            submission = Submission.objects.create(user=request.user, poll=poll)
            
            for question in poll.questions.all():
                answer_id = form.cleaned_data.get(f"question_{question.id}")
                answer = Answer.objects.get(pk=answer_id)
                SubmittedAnswer.objects.create(submission=submission, answer=answer)
            return redirect('myApp:home')
    else:
        form = PollSubmissionForm(poll=poll)
    return render(request, 'myApp/poll.html', {'poll':poll, 'form':form})
        

@login_required
def create_poll(request):
    if request.method == "POST":
        title = request.POST.get("poll_title")
        poll = Poll.objects.create(title=title)

        # Go through all POST items
        questions = {}
        answers = {}

        for key, value in request.POST.items():
            if key.startswith("question_"):
                q_index = key.split("_")[1]
                questions[q_index] = value
            elif key.startswith("answer_"):
                _, q_index, a_index = key.split("_")
                answers.setdefault(q_index, []).append(value)

        for q_index, q_body in questions.items():
            question = Question.objects.create(body=q_body, poll=poll)
            for a_body in answers.get(q_index, []):
                Answer.objects.create(body=a_body, question=question)

        return redirect('myApp:home')

    return render(request, "myApp/create_poll.html")