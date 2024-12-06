from django.db import models
from user.models import UserProfile

class Swipe(models.Model):
    SWIPE_CHOICES = [
                     ('like','Like'),
                     ('dislike','Dislike')
                     ]
    swiper = models.ForeignKey( UserProfile, related_name='swipes_made', on_delete=models.CASCADE )
    swiped = models.ForeignKey( UserProfile, related_name='swipes_received', on_delete=models.CASCADE )
    swipe_type = models.CharField( max_length=10,choices=SWIPE_CHOICES )
    timestamp = models.DateTimeField( auto_now_add=True )
    
    def __str__(self):
        return f"{self.swiper} -> {self.swipe_type} -> {self.swiped}"

class Match(models.Model):
    user1 = models.ForeignKey( UserProfile, related_name='match_initiated', on_delete=models.CASCADE )
    user2 = models.ForeignKey( UserProfile, related_name='matches_received', on_delete=models.CASCADE )
    timestamp = models.DateTimeField( auto_now_add=True )

    def __str__(self):
        return f"Мэтч между {self.user1} и {self.user2}"