from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Character

@login_required
def character_list(request):
    characters = Character.objects.filter(player=request.user)  # Filter characters by the logged-in user
    return render(request, 'characters/character_list.html', {'characters': characters})


@login_required
def character_detail(request, character_name):
    character = get_object_or_404(Character, name=character_name, player=request.user)
    return render(request, 'characters/character_detail.html', {'character': character})


def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('character_list')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'characters/login.html')