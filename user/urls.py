from django.urls import path
from .views import *

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('register', register, name='register'),
    path('welcome', welcome, name='welcome'),

    path('home', home, name='home')
]
