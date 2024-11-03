from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Campaign, Character
from .forms import CharacterCreationForm, CampaignCreationForm

@login_required
def character_list(request):
    # Get all characters belonging to the logged-in user
    user_characters = Character.objects.filter(player=request.user)
    
    # Get campaigns where any of the user's characters are present
    campaigns_with_user_characters = Campaign.objects.filter(characters__in=user_characters).distinct()

    # Get campaigns where the user is the campaign master
    campaigns_mastered_by_user = Campaign.objects.filter(campaign_master=request.user)

    # Combine both querysets and remove duplicates
    all_campaigns = campaigns_with_user_characters.union(campaigns_mastered_by_user)
    
    return render(request, 'characters/character_list.html', {
        'user_characters': user_characters,
        'all_campaigns': all_campaigns,
        'user_is_master': campaigns_mastered_by_user,
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
def delete_character(request, character_name):
    character = get_object_or_404(Character, name=character_name, player=request.user)
    
    if request.method == "POST":
        character.delete()
        return redirect("characters:character_list")  # Redirect to the character list after deletion

    # If someone tries to access the URL with GET, just redirect to the character list
    return redirect("characters:character_list")


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


@login_required
def create_campaign(request):
    if request.method == "POST":
        form = CampaignCreationForm(request.POST)
        if form.is_valid():
            # Save the campaign, setting the campaign master to the current user
            campaign = form.save(commit=False)
            campaign.campaign_master = request.user
            campaign.save()
            return redirect("characters:campaign_detail", campaign_name=campaign.name)
    else:
        form = CampaignCreationForm()

    return render(request, "characters/create_campaign.html", {"form": form})


@login_required
def delete_campaign(request, campaign_name):
    campaign = get_object_or_404(Campaign, name=campaign_name)
    
    if request.method == "POST":
        campaign.delete()
        return redirect("characters:character_list")  # Redirect to the character list after deletion

    # If someone tries to access the URL with GET, just redirect to the character list
    return redirect("characters:character_list")