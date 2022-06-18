import profile
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import NeighbourHood, Profile, Updates
from .forms import CreateNeigbourhoodForm, RegisterForm, ProfileUpdateForm
from .email import welcome


# Create your views here.
def login_user(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User doesnt exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'incorect username or password')
    ctx = {'page': page}
    return render(request, 'mainapp/auth.html', ctx)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    form  = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            recipient = User(username=username, email=email)
            welcome(username, email)

            profile= Profile.objects.create(owner=user)
            profile.save()

            return render(request, 'mainapp/success.html')
    ctx = {'form': form}
    return render(request, 'mainapp/auth.html', ctx)

def home(request):
    ctx = {}
    return render(request, 'mainapp/index.html', ctx)

@login_required(login_url='login')
def contact(request):
    ctx = {}
    return render(request, 'mainapp/contact.html', ctx)

def about(request):
    ctx = {}
    return render(request, 'mainapp/about.html', ctx)

@login_required(login_url='login')
def neighborhoods(request):
    neigbourhoods = NeighbourHood.objects.all()
    member = Profile.objects.get(owner = request.user)
    context = {'neigbourhoods': neigbourhoods, 'member': member}
    return render(request, 'mainapp/neigbourhood.html', context)

def single_hood(request, name):
    newneigbour = NeighbourHood.objects.get(name = name)
    updates = Updates.objects.filter(hood = newneigbour)
    current_user = Profile.objects.get(owner = request.user)

    if request.method == 'POST':
        display = Profile.objects.get(owner = request.user)
        title = request.POST.get('title')
        body = request.POST.get('body')
        new_updates = Updates.objects.create(title = title, body =body, display = display, newneigbour =newneigbour)
        new_updates.save()

    ctx = {'newneigbour': newneigbour, 'current_user': current_user, 'updates':updates}
    return render(request, 'mainapp/self.html', ctx)

@login_required(login_url='login')
def join_neighborhood(request, name):
    page = 'join'
    hood = get_object_or_404(NeighbourHood, name=name)
    if request.method == 'POST':
        user = Profile.objects.get(owner =request.user)
        user.hood = hood
        user.save()
        messages.success(request, 'You have successfully joined')
        return redirect('hood', hood.name)
    ctx = {'page':page, 'obj': hood}
    return render(request, 'hoodapp/join.html', ctx)

@login_required(login_url='login')
def leave_neighborhood(request, name):
    hood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.hood = None
    request.user.profile.save()
    return redirect('hood')

@login_required(login_url='login')
def create_neighborhood(request):
    form  = CreateNeigbourhoodForm()
    if request.method == "POST": 
        form = CreateNeigbourhoodForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            img = form.cleaned_data['img']
            data = NeighbourHood.objects.create(name=name, admin=request.user, location=location, img=img)
            data.save()
            return redirect('hoods')
    ctx = {'form': form}
    return render(request, 'hoodapp/create-hood.html', ctx)

def user_profile(request):
    profile = Profile.objects.get(owner = request.user)
    ctx = {'profile': profile}
    return render(request, 'hoodapp/profile.html', ctx)

def update_profile(request):
    profile = Profile.objects.get(owner = request.user)
    form = ProfileUpdateForm(instance=profile)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile, )
        if form.is_valid():
            form.save()
            return redirect('profile')

    ctx = {'profile': profile, 'form':form}
    return render(request, 'hoodapp/update-profile.html', ctx)
