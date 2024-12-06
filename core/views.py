from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from user.models import UserProfile
from .models import Swipe, Match
from django.contrib.auth.decorators import login_required


# Create your views here.

def main(request):
    return render(request, '../templates/main.html')

@login_required
def stream(request):
    swipe_type = None
    MESSAGE = None

    # Получить профиль пользователя
    profile = get_object_or_404(UserProfile, user=request.user)

    # Определяем противоположный пол
    opposite_gender = 'F' if profile.gender == 'M' else 'M'

    # Получить список уже оцененных анкет
    swiped_ids = Swipe.objects.filter(swiper=profile).values_list('swiped_id',flat=True)

    # Получить анкету которую будем оценивать на странице
    current_profile = UserProfile.objects.exclude(id=profile.id).filter(gender=opposite_gender).exclude(id__in=swiped_ids).order_by('?').first()

    # Получить список мэтчей в которых есть пользователь
    matches = Match.objects.filter( Q(user1=profile) | Q(user2=profile) )

    # Получить список мэтчей
    matched_profiles = UserProfile.objects.filter(id__in=[match_profile.user1.id if match_profile.user1 != profile else match_profile.user2.id  for match_profile in matches])

    if request.method == 'GET':

        # Обрабатываем исключение когда нет оцениваемой анкеты
        if not current_profile:
            MESSAGE = 'Все анкеты просмотрены!'

            context = {
                        'profile':profile,
                        'opposite_gender':opposite_gender,
                        'swiped_ids' : None,
                        'message': MESSAGE,
                        'current_profile':current_profile,
                        'matched_profiles':matched_profiles
                        }
            
            return render(request, 'stream.html', context)

        context = {
                'profile':profile,
                'opposite_gender':opposite_gender,
                'swiped_ids' : swiped_ids,
                'message': MESSAGE,
                'current_profile':current_profile,
                'matched_profiles':matched_profiles,
                'swipe_type':swipe_type
                }

        return render(request, 'stream.html', context)

@login_required
def like(request, current_profile_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    current_profile = UserProfile.objects.get(id=current_profile_id)

    redirect_url = request.GET.get('next')

    Swipe.objects.create(
                         swiper = profile,
                         swiped = current_profile,
                         swipe_type = 'like'
                         )
    
    mutual_like = Swipe.objects.filter(
                                       swiper = current_profile,
                                       swiped = profile,
                                       swipe_type = 'like'
                                       )
                
    if mutual_like:
        Match.objects.create(
                             user1 = profile,
                             user2 = current_profile
                             )
    
    return redirect(redirect_url)

@login_required
def dislike(request, current_profile_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    current_profile = UserProfile.objects.get(id=current_profile_id)

    redirect_url = request.GET.get('next')

    Swipe.objects.create(
                         swiper = profile,
                         swiped = current_profile,
                         swipe_type = 'dislike'
                         )
    
    return redirect(redirect_url)
    