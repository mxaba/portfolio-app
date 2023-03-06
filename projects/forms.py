from django import forms
from .models import Project, Tag
from ckeditor.widgets import CKEditorWidget


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
