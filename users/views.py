from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required
from .utils import searchProfile, paginateProfile

from .models import Profile,Message
# Create your views here.

# authenticating login page


def loginUser(request):
    page = 'login'
    # if already loged in then prevent it to go to login page from url
    if request.user.is_authenticated:
        return redirect('profile')
    # POST is obtained from login form
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
    # check username is already registered
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")
    # if user is already registered then authenticate/check it with its password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # if user is correct then login the user

            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else "account")
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, 'users/login-register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, "User is logged out.")
    return redirect('profile')


def profile(request):
    profiles, search_query = searchProfile(request)
    custom_range, profiles = paginateProfile(request, profiles, 3 )
    context = {'profiles': profiles, 'search': search_query,
               'custom_range': custom_range}

    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skills_set.exclude(description__exact="")
    otherSkills = profile.skills_set.filter(description="")
    context = {'profile': profile, 'topSkills': topSkills,
               'otherSkills': otherSkills}
    return render(request, 'users/user-profiles.html', context)


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # saving the form but not sending to the database so commit=False
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User account has been created")
            login(request, user)
            return redirect("account")
        else:
            messages.error(
                request, "An error has occurred during registration")

    context = {'page': page, 'form': form}
    return render(request, 'users/login-register.html', context)

# creating user ACCOUNT


@login_required(login_url='login')
def accountUser(request):
    # getting one to one relation of profile and user
    profile = request.user.profile
    skills = profile.skills_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/user-account.html', context)

# editing the user account


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile-form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            # setting the skill of the owner profile
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added succesfully!")
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    # prefill the form with the instance method
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():

            skill.save()
            messages.success(request, "Skill was updated succesfully!")

            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    # prefill the form with the instance method
    form = SkillForm()
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill was deleted succesfully!")

        return redirect('account')
    context = {'form': skill}
    return render(request, 'delete-template.html', context)

@login_required(login_url='login')
def inbox(request):
    profile=request.user.profile
    # instead of message_set.all messages is used which is the related_name
    messageRequests=profile.messages.all()
    unreadCount=messageRequests.filter(is_read=False).count()

    context={'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render(request, 'users/inbox.html',context)


@login_required(login_url='login')
def viewMessage(request,pk):
    profile=request.user.profile
    message=profile.messages.get(id=pk)
    if message.is_read==False:
        message.is_read=True
        message.save()
    context={'message':message}
    return render(request, 'users/message.html',context)


def createMessage(request,pk):
    # from the create-message url/id is taken and searched in profile
    receiver=Profile.objects.get(id=pk)
    form=MessageForm()
    try:
        sender=request.user.profile
    except:
        sender=None

    if request.method=="POST":
        form=MessageForm(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.sender=sender
            message.receiver=receiver
            
            if sender:
                message.name=sender.name
                message.email=sender.email
            message.save()
            messages.success(request,'Your message was sent successfully')
            return redirect('user-profile',pk=receiver.id)
    context={'receiver':receiver,'form':form}
    return render(request, 'users/message_form.html',context)
    