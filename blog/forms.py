from django import forms

from . import models

class CommentsForm(forms.ModelForm):
    class Meta:
        model=models.Comment
        exclude=['post']
        labels={
            "user_name":"Your Name",
            "user_email":"Email",
            "text":"Your Comment"
        }