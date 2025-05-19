from django.contrib import admin
from .models import Poll, Answer, Question, Submission, SubmittedAnswer

admin.site.register(Poll)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(SubmittedAnswer)
admin.site.register(Submission)