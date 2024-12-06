from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=280)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self,request=None,*args,**kwargs):
        self.request = request
        self.user = None

        super(LoginForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    def get_user(self):
        return self.user
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        self.user = authenticate(self.request, username=username, password=password)
        if not self.user:
            raise ValidationError('Неверный логин или пароль')

class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(widget=forms.PasswordInput,label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')
    
    def __init__(self,*args,**kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise ValidationError('Пароли не совпадают')
        
        return password2
    
    def clean_username(self):
        username = self.cleaned_data['username']
        User = get_user_model()

        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже есть')
        
        return username
    
class UserProfileForm(forms.Form):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    bio = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Напиши немного о себе'}),
        label="О себе"
    )
    age = forms.IntegerField(
        min_value=18,
        max_value=88,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ваш возраст'}),
        label="Возраст"
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Пол"
    )
    photo = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Фотография"
    )
    link = forms.CharField(
        max_length=140,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ссылка на ваш сайт или соцсеть'}),
        label="Ссылка"
    )