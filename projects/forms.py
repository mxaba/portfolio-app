from django import forms
from .models import Project, Tag
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Project
        fields = ['title', 'content', 'thumbnail', 'active', 'featured', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super().__init__(*args, **kwargs)
        if author:
            self.fields['author'] = forms.ModelChoiceField(
                queryset=User.objects.filter(pk=author.pk),
                widget=forms.HiddenInput(),
            )
        else:
            self.fields['author'] = forms.ModelChoiceField(
                queryset=User.objects.all(),
                widget=forms.Select(),
            )
    
    def save(self, *args, **kwargs):
        if not self.instance.pk:
            self.instance.author = kwargs.pop('author', None)
        super().save(*args, **kwargs)