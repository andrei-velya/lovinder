from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('stream', stream, name='stream'),
    path('like/<int:current_profile_id>',like,name='like'),
    path('dislike/<int:current_profile_id>',dislike,name='dislike')

]
