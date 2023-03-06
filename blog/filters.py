import django_filters
from django import forms
from .models import *
from django.db.models import Q


class PostFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter', label='Search for specific post',
                                  widget=forms.TextInput(attrs={'placeholder': u"\U0001F50D"}))
    # title = django_filters.CharFilter(field_name='title', lookup_expr="icontains", label='Title')
    categories = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                          widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = ['q', 'categories']

    def my_custom_filter(self, queryset, name, value):
        return Post.objects.filter(Q(title__icontains=value) | Q(author__username__icontains=value) |
                                   Q(categories__name__icontains=value)).distinct()
