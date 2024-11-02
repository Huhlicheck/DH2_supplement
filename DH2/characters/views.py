from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Campaign, Character
from .forms import CharacterCreationForm

@login_required
def character_list(request):
    # Get all characters belonging to the logged-in user
    user_characters = Character.objects.filter(player=request.user)
    
    # Get campaigns where any of the user's characters are present
    campaigns_with_user_characters = Campaign.objects.filter(characters__in=user_characters).distinct()
    
    return render(request, 'characters/character_list.html', {
        'user_characters': user_characters,
        'campaigns_with_user_characters': campaigns_with_user_characters,
    })


@login_required
def character_detail(request, character_name):
    character = get_object_or_404(Character, name=character_name, player=request.user)
    return render(request, 'characters/character_detail.html', {'character': character})


@login_required
def create_character(request):
    if request.method == "POST":
        form = CharacterCreationForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.player = request.user  # Set the logged-in user as the character's player
            character.save()
            return redirect("characters:character_detail", character_name=character.name)  # Redirect to the character detail after creation
    else:
        form = CharacterCreationForm()  # Show empty form for GET request
    
    return render(request, "characters/create_character.html", {"form": form})


@login_required
def campaign_detail(request, campaign_name):
    campaign = get_object_or_404(Campaign, name=campaign_name)
    characters = campaign.characters.exclude(player=campaign.campaign_master) # Separate characters based on the campaign master and other players
    master_character = campaign.characters.filter(player=campaign.campaign_master).first()  # Get master's character if it exists
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
        "master_character": master_character,  # Pass the master's character separately
    })


def create_campaign(request):
    if request.method == "POST":
        form = CampaignCreationForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.player = request.user  # Set the logged-in user as the character's player
            character.save()
            return redirect("characters:character_list")  # Redirect to the character list after creation
    else:
        form = CampaignCreationForm()  # Show empty form for GET request
    
    return render(request, "characters/create_campaign.html", {"form": form})