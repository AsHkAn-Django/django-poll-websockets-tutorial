from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Question, Poll, Submission, Answer, SubmittedAnswer
from .forms import PollSubmissionForm , PollForm, QuestionForm, AnswerForm, QuestionFormSet
from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



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

            # Update poll vote count
            poll.num_votes += 1
            poll.save()

            # Notify WebSocket group
            channel_layer = get_channel_layer()
            print(f"[VIEW] Broadcasting to poll_{poll.id}: {poll.num_votes}")   # ← log
            async_to_sync(channel_layer.group_send)(
                f'poll_{poll.id}',            # must match the consumer’s group_name
                {
                    'type': 'vote_update',     # routes to PollConsumer.vote_update
                    'num_votes': poll.num_votes,
                }
            )

            return redirect('myApp:home')
    else:
        form = PollSubmissionForm(poll=poll)

    return render(request, 'myApp/poll.html', {'poll': poll, 'form': form})
  

@login_required
def create_poll(request):
    if request.method == "POST":
        title = request.POST.get("poll_title")
        poll = Poll.objects.create(title=title)

        questions = {}  # Will store questions like {"0": "What's your favorite fruit?"}
        answers = {}    # Will store answers like {"0": ["Apple", "Banana"], "1": ["Water", "Juice"]}
        
        # Go through all POST items
        for key, value in request.POST.items():
            if key.startswith("question_"):
                # key is the input name (e.g., "question_0")
                # value is the user input (e.g., "What's your favorite color?")
                q_index = key.split("_")[1]
                # Extract the question index from the key (e.g., "question_0" → "0")
                questions[q_index] = value
            elif key.startswith("answer_"):
                # answer_0_0 → q_index = "0", a_index = "0"
                _, q_index, a_index = key.split("_")
                # Ensure answers[q_index] is a list, then append the answer body
                answers.setdefault(q_index, []).append(value)

        for q_index, q_body in questions.items():
            question = Question.objects.create(body=q_body, poll=poll)
            for a_body in answers.get(q_index, []):
                Answer.objects.create(body=a_body, question=question)

        return redirect('myApp:home')

    return render(request, "myApp/create_poll.html")