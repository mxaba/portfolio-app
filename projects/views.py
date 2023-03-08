from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Project, Tag
from .forms import ProjectForm
from .decorators import *


def projects(request):
    print(request.user)
    user = get_object_or_404(User, username=request.user)
    all_project = Project.objects.filter(active=True, author=user)
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
    project = get_object_or_404(Project, slug=slug)

    context = {'project': project}
    return render(request, 'projects/project_details.html', context)


@login_required
def project_create(request):
    form = ProjectForm()

    print(request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, request=request)
        print(form.is_valid())
        if form.is_valid():
            form.instance.author = request.user
            instance = form.save()
            print(instance)
            return redirect('projects:project-details', slug=instance.slug)
        print(form.errors)

    context = {'form': form, 'section_title': 'Add Project'}
    return render(request, 'projects/project_form.html', context)


@login_required
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


@login_required
def project_delete(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.method == 'POST':
        project.delete()
        messages.success(request, f'Project deleted successfully')
        return redirect('projects:projects')

    context = {'project': project}
    return render(request, 'projects/project_confirm_delete.html', context)
