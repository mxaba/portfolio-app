from django.contrib import admin
from .models import Tag, Project

admin.site.register(Tag)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'active', 'featured']
