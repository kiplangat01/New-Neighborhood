from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import NeighbourHood, Profile



class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, label='',widget=forms.EmailInput(attrs={'class': 'form-control mb-4', 'placeholder': 'email'}))
    username =forms.CharField(max_length=200, label='',widget=forms.TextInput(attrs={'class': 'form-control mb-4','placeholder': 'username'}))
    password1 = forms.CharField(max_length=200,label='',widget=forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder': 'password'}))
    password2 = forms.CharField(max_length=200, label='',widget=forms.PasswordInput(attrs={'class': 'form-control mb-4','placeholder': 'confirm password'}))
    
    class Meta():
       model=User
       fields = ['email', 'username', 'password1', 'password2']


class CreateNeighbourhoodForm(ModelForm):
    name = forms.CharField(max_length=200, label='',widget=forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'name'}))
    location =forms.CharField(max_length=200, label='',widget=forms.TextInput(attrs={'class': 'form-control mb-4','placeholder': 'location'}))
    img = forms.FileField(max_length=200,label='',widget=forms.FileInput(attrs={'class': 'form-control mb-4', 'placeholder': 'hood image'}))
    
    class Meta():
        model = NeighbourHood
        fields = ['name', 'location', 'img']

class ProfileUpdateForm(ModelForm):
    bio = forms.CharField(max_length=200, label='',widget=forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'bio'}))
    photo = forms.FileField(max_length=200,label='',widget=forms.FileInput(attrs={'class': 'form-control mb-4', 'placeholder': 'profile photo'}))
    
    class Meta():
        model = Profile
        fields = ['bio', 'photo']