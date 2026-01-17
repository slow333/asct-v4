import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse

class Question(models.Model):
    question_text = models.CharField(
        max_length=200, verbose_name='질문',
        help_text='질문을 션택하세요.'
    )
    pub_date = models.DateTimeField('생성날짜', default=timezone.now)
    blog = models.ForeignKey('blog.Post', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE )
    choice_text = models.CharField(
        max_length=200,
        verbose_name='답변',
        help_text='답변을 입력하세요.',
        null=True, blank=True,
    )
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text

# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name
