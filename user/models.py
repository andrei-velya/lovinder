from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class UserProfile(models.Model):
    GENDER_CHOICES = [
                      ('M','Мужской'),
                      ('F','Женский')
                      ]
    user = models.OneToOneField(
                                User,
                                on_delete=models.CASCADE
                                )
    bio = models.TextField( max_length = 500 )
    age = models.PositiveIntegerField( default=20,validators=[ MinValueValidator(18), MaxValueValidator(88) ] )
    gender = models.CharField( max_length=1,choices=GENDER_CHOICES )
    photo = models.ImageField( upload_to='profile_pics/' )
    link = models.CharField( max_length = 140 )
    
    def __str__(self):
        return f"Профиль {self.user.username}"