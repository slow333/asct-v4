from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'blog']
        widgets = {
            'question_text': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '질문을 입력하세요.'}),
            'blog': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'question_text': '질문',
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(
                attrs={'class': 'form-control',}),
        }
