from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Character

@login_required
def character_list(request):
    characters = Character.objects.filter(player=request.user)  # Filter characters by the logged-in user
    return render(request, 'characters/character_list.html', {'characters': characters})


@login_required
def character_detail(request, character_name):
    character = get_object_or_404(Character, name=character_name, player=request.user)
    return render(request, 'characters/character_detail.html', {'character': character})