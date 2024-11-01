from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Campaign, Character

@login_required
def character_list(request):
    characters = Character.objects.filter(player=request.user)  # Filter characters by the logged-in user
    return render(request, 'characters/character_list.html', {'characters': characters})


@login_required
def character_detail(request, character_name):
    character = get_object_or_404(Character, name=character_name, player=request.user)
    return render(request, 'characters/character_detail.html', {'character': character})

@login_required
def campaign_detail(request, campaign_name):
    campaign = get_object_or_404(Campaign, name=campaign_name)
    characters = campaign.characters.exclude(player=campaign.campaign_master)  # Exclude campaign master’s character
    is_master = request.user == campaign.campaign_master  # Check if the user is the campaign master

    if request.method == "POST" and is_master:
        character_id = request.POST.get("character_id")
        experience_points = int(request.POST.get("experience_points"))
        character = get_object_or_404(Character, id=character_id)
        campaign.assign_experience(character, experience_points)
        return redirect("characters:campaign_detail", campaign_name=campaign.name)

    return render(request, "characters/campaign_detail.html", {
        "campaign": campaign,
        "characters": characters,
        "is_master": is_master,
    })