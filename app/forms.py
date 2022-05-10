from django import forms
from django.forms import ModelForm
from app.models import Category, Question, Reply

class QuestionRoom(ModelForm):
    class Meta:
        model = Question
        fields = ['title','category','content']
        labels = {
            'title': 'Sarlavha',
            'category': 'Tur',
            'content': 'Asosiy qism'
        }
    def __init__(self, *args, **kwargs):
        super(QuestionRoom, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'


class ReplyRoom(ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        labels = {
            'content': 'Javob'
        }
