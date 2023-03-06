from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Project, Tag
from .forms import ProjectForm
from .decorators import *


def projects(request):
    all_project = Project.objects.filter(active=True)
    tags = Tag.objects.all()

    category = request.GET.get('q')

    if category is None:
        all_project = all_project
    else:
        category = category.strip()
        all_project = all_project.filter(Q(tags__name__icontains=category))

    context = {'all_project': all_project, 'tags': tags, 'category': category}
    return render(request, 'projects/projects.html', context)


def project_details(request, slug):
    # project = Project.objects.filter(slug=slug).first()
    project = get_object_or_404(Project, slug=slug)

    context = {'project': project}
    return render(request, 'projects/project_details.html', context)


@admin_only
def project_create(request):
    form = ProjectForm()

    print(form)
    print(request)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            instance = form.save()
            return redirect('projects:project-details', slug=instance.slug)

    context = {'form': form, 'section_title': 'Add Project'}
    return render(request, 'projects/project_form.html', context)


@admin_only
def project_update(request, slug):
    project = get_object_or_404(Project, slug=slug)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            instance = form.save()
            messages.success(request, f'Project Updated')
            return redirect('projects:project-details', slug=instance.slug)

    context = {'form': form, 'section_title': 'Update Project'}
    return render(request, 'projects/project_form.html', context)


@admin_only
def project_delete(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.method == 'POST':
        project.delete()
        messages.success(request, f'Project deleted successfully')
        return redirect('projects:projects')

    context = {'project': project}
    return render(request, 'projects/project_confirm_delete.html', context)
