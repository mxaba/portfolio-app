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
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        project = super().save(commit=False)
        if not project.author_id:
            project.author = self.request.user
        if commit:
            project.save()
        return project