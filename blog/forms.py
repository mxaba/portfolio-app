from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        labels = {'sub_heading': 'Sub Heading'}
        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }
        exclude = ['author', 'created', 'featured', 'slug']
