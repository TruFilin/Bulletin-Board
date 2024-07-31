from django import forms
from .models import Announcement, Response, News

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'category', 'image', 'video']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
