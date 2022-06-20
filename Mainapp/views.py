from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import messages
from .models import NeighbourHood, Profile, Updates
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

            return render(request, 'main/index.html')
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
    newnmember = NeighbourHood.objects.get(name = name)
    updates = Updates.objects.filter(neighborhood = newnmember)
    current_user = Profile.objects.get(user = request.user)

    if request.method == 'POST':
        display = Profile.objects.get(user = request.user)
        title = request.POST.get('title')
        body = request.POST.get('body')
        new_updates = Updates.objects.create(title = title, body =body, display = display, newnmember =newnmember)
        new_updates.save()

    context = {'newnmember': newnmember, 'current_user': current_user, 'updates':updates}
    return render(request, 'main/self.html', context)

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
        return redirect('neighbourhood')
    ctx = {'page': page, 'neighbourhood': neighbourhood}
    return render(request, 'main/join.html', ctx)


@login_required(login_url='login')
def leave_neighborhood(request, name):
    neighbourhood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.nei = None
    request.user.profile.save()
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
            return redirect('hoods')
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
