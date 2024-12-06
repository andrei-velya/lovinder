from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, UserProfileForm
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

def login(request):
    form = LoginForm(request,request.POST)

    if request.method == 'POST':
        form = LoginForm(request,request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request,user)

            return redirect('stream')
    
    return render(request,'user/login.html', {'form':form})


def logout(request):
    auth_logout(request)
    return redirect('main')


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('Надо создать пользователя')

            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']

            User = get_user_model()
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()

            UserProfile.objects.create(user=user)

            user = authenticate(request, username=username, password=password)
            auth_login(request=request, user=user)

            return redirect('welcome')
    
    return render(request, 'user/register.html', {'form':form})

@login_required
def home(request):
    profile = request.user.profile
    context = {
               }
    return render(request, 'user/home.html', context)


@login_required
def welcome(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохраняем данные в модель
            profile = UserProfile.objects.get(user=request.user)
            profile.bio = form.cleaned_data['bio']
            profile.age = form.cleaned_data['age']
            profile.gender = form.cleaned_data['gender']
            profile.photo = form.cleaned_data['photo']
            profile.link = form.cleaned_data['link']
            profile.save()
            return redirect('stream')  # Перенаправляем на главную
    else:
        # Если данные уже существуют, заполняем форму их значениями
        profile = UserProfile.objects.get(user=request.user)
        form = UserProfileForm(initial={
            'bio': profile.bio,
            'age': profile.age,
            'gender': profile.gender,
            'link': profile.link,
        })

    return render(request, 'user/welcome.html', {'form': form})