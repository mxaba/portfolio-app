from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Post
        fields = '__all__'
        labels = {'sub_heading': 'Sub Heading'}
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
             'content': forms.Textarea(attrs={'rows': 5}),
            'thumbnail': forms.ClearableFileInput(attrs={'multiple': True}),
        }
