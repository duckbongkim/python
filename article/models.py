from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name = 'author_queserion')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True) ## blank>> form.is_valid(): 유효성 검사를 건너 띔
    voter = models.ManyToManyField(User, related_name='voter_question')
    
    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modity_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')
    
    def __str__(self):
        return self.content[:20]  # 내용의 첫 20자만 표시

class Test(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(null=True)
