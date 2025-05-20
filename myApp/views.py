from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Question, Poll, Submission, Answer, SubmittedAnswer
from .forms import PollSubmissionForm
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
        
        


