from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import messages
from .models import Business, NeighbourHood, Profile, Updates
from .forms import CreateNeighbourhoodForm, RegisterForm, ProfileUpdateForm
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
    context = {'page': page}
    return render(request, 'main/user.html', context)

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
            messages.success(request, f'Account created you can now login')

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            recipient = User(username=username, email=email)
            welcome(username, email)

            profile= Profile.objects.create(user=user)
            profile.save()
            
            page = 'register'
            return render(request, 'main/index.html' ,{'page': page})
    context = {'form': form}
    return render(request, 'main/user.html', context)

def home(request):
    context = {}
    return render(request, 'main/index.html', context)




@login_required(login_url='login')
def neighborhoods(request):
    neighbourhood = NeighbourHood.objects.all()
    member = Profile.objects.get(user = request.user)
    context = {'neigbourhoods': neighbourhood, 'member': member}
    return render(request, 'main/neigbourhood.html', context)

def self_neigbourhood(request, name):
    neighbourhood = NeighbourHood.objects.get(name=name)
    updates = Updates.objects.filter(neighbourhood=neighbourhood)
    business = Business.objects.filter(neighbourhood=neighbourhood)
    current_user = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        body = request.POST.get('body')

    ctx = {'neighbourhood': neighbourhood, 'current_user': current_user, 'updates': updates, 'business': business}
    return render(request, 'main/self.html', ctx)

@login_required(login_url='login')
def view_neighbourhood(request, name):
    page = 'view'
    neighbourhood = get_object_or_404(NeighbourHood, name=name)
    context = {'page':page, 'neighbourhood': neighbourhood}
    return render(request, 'main/join.html', context)


@login_required(login_url='login')
def join_neighbourhood(request, name):
    page = 'join'
    neighbourhood = get_object_or_404(NeighbourHood, name=name)
    if request.method == 'POST':
        user = Profile.objects.get(user=request.user)
        user.neighbourhood = neighbourhood
        user.save()
        messages.success(request, 'You have successfully joined')
        return redirect('selected', neighbourhood.name)
    ctx = {'page': page, 'neighbourhood': neighbourhood}
    return render(request, 'main/join.html', ctx)


@login_required(login_url='login')
def leave_neighbourhood(request, name):
    profile = Profile.objects.get(user = request.user)
    neighborhood = get_object_or_404(NeighbourHood, name=name)
    profile.hood = None
    profile.save()
    messages.success(request, 'successfully left the neigbourhood')
    return redirect('neighbourhood')

@login_required(login_url='login')
def create_neighbourhood(request):
    page = 'create'
    form  = CreateNeighbourhoodForm()
    if request.method == "POST": 
        form = CreateNeighbourhoodForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            img = form.cleaned_data['img']
            data = NeighbourHood.objects.create(name=name, admin=request.user, location=location, img=img)
            data.save()
            return redirect('neighbourhood')
    context = {'form': form}
    return render(request, 'main/create.html', context)

def user_profile(request):
    profile = Profile.objects.get(user = request.user)
    context = {'profile': profile}
    return render(request, 'main/profile.html', context)

def update_profile(request):
    profile = Profile.objects.get(user = request.user)
    form = ProfileUpdateForm(instance=profile)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile, )
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'profile': profile, 'form':form}
    return render(request, 'main/updateprofile.html', context)

def add_updates(request, name):
    page = 'updates'
    neighbourhood = NeighbourHood.objects.get(name=name)
    if request.method == 'POST':
        displayer = Profile.objects.get(user=request.user)
        title = request.POST.get('title')
        body = request.POST.get('body')
        new_updates = Updates.objects.create(
           displayer=displayer, title=title, body=body,  neighbourhood=neighbourhood)
        new_updates.save()
        context = {'neighbourhood': neighbourhood}
        return redirect('selected', neighbourhood.name)
    context = {'page':page}
    return render(request, 'main/post.html', context)

def add_business(request, name):
    page = 'business'
    neighbourhood = NeighbourHood.objects.get(name=name)
    if request.method == 'POST':
        user = Profile.objects.get(user=request.user) 
        business_name = request.POST.get('name')
        location = request.POST.get('location')
        contact = request.POST.get(' contact')
        new_business = Business.objects.create(user=user, name=business_name, location=location,  contact= contact, neighbourhood=neighbourhood)
        new_business.save()
        return redirect('connect', neighbourhood.name)
    context = {'page':page}
    return render(request, 'main/post.html', context)