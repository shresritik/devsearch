from django.shortcuts import render, redirect
from .models import *
from .forms import ProjectForm,ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .utils import searchProject, paginateProject
from django.contrib import messages
# Create your views here.


def projects(request):
    projectList, search_query = searchProject(request)
    custom_range, projectList = paginateProject(request, projectList, 6)

    context = {'projects': projectList,
               'search': search_query,  'custom_range': custom_range}

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form=ReviewForm()
    if request.method=="POST":
        form=ReviewForm(request.POST)
        review=form.save(commit=False)
        review.project=projectObj
        review.owner=request.user.profile
        review.save()
        projectObj.getVoteCount
        messages.success(request,"Review was successfully submitted")
        return redirect('project',pk=projectObj.id)
    return render(request, 'projects/project.html', {'project': projectObj,'form':form})

# restricting user until loggedin


@login_required(login_url='login')
def createForm(request):
    profile = request.user.profile

    form = ProjectForm()
    if request.method == "POST":
        newtags=request.POST.get("newtags").replace(","," ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                # iterate through the newtags and check if it is already created or needs to be
                tag,created=Tag.objects.get_or_create(name=tag)
                # adding tags inside the projects model from many to many relation
                project.tags.add(tag)

            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def updateForm(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        # get the tags and if there is a comma then replace it with space and with split method it will make into array
        newtags=request.POST.get("newtags").replace(","," ").split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            for tag in newtags:
                # iterate through the newtags and check if it is already created or needs to be
                tag,created=Tag.objects.get_or_create(name=tag)
                # adding tags inside the projects model from many to many relation
                project.tags.add(tag)
            return redirect('account')
    context = {'form': form,'project':project}
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def deleteForm(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')
    context = {'form': project}
    return render(request, 'delete-template.html', context)
