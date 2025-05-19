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
    

class Response(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_surveys', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='answer_surveys', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} chose {self.answer.body}"