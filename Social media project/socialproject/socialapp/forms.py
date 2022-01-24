from django import forms
from .models import Post, Comment, Profile

class Post_form(forms.ModelForm):
  text = forms.CharField(label='', widget = forms.Textarea(attrs={'row':3, 'placeholder':'say something'}))
  class Meta:
    model = Post
    fields = ['title', 'text', 'image']
    
class Comment_form(forms.ModelForm):
  comments = forms.CharField(label='', widget = forms.Textarea(attrs={'row':3, 'placeholder':'say something'}))
  class Meta:
    model = Comment
    fields = ['comments']

class Profile_form(forms.ModelForm):
  class Meta:
    model = Profile
    fields = '__all__'