from django.db import models
from django.conf import settings


class Poll(models.Model):
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    body = models.CharField(max_length=150)
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body
    

class Answer(models.Model):
    body = models.CharField(max_length=150)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.body
    

class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class SubmittedAnswer(models.Model):
    submission = models.ForeignKey(Submission, related_name='answers', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
