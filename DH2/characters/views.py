from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Campaign, Character, Skill, CharacterSkill
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
    all_campaigns_with_user = campaigns_with_user_characters.union(campaigns_mastered_by_user)
    
    return render(request, 'characters/character_list.html', {
        'user_characters': user_characters,
        'all_campaigns': all_campaigns_with_user,
        'user_is_master': campaigns_mastered_by_user,
    })


@login_required
def character_detail(request, character_name):
    character = get_object_or_404(Character, name=character_name, player=request.user)
    
  # Filter CharacterSkill instances for the character with level >= 0
    visible_skills = CharacterSkill.objects.filter(character=character, level__gte=0)

    context = {
        "character": character,
        "visible_skills": visible_skills,
    }
    return render(request, "characters/character_detail.html", context)



@login_required
def skill_upgrade_list(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    skills = Skill.objects.all()  # Get all skills

    # Create a list of (skill, character_skill) pairs
    skill_data = [
        (skill, character.skills.filter(skill=skill).first() or CharacterSkill(skill=skill, character=character))
        for skill in skills
    ]

    if request.method == "POST":
        skill_id = request.POST.get("skill_id")
        skill = get_object_or_404(Skill, id=skill_id)

        # Get or create the CharacterSkill instance for the selected skill
        character_skill, created = CharacterSkill.objects.get_or_create(character=character, skill=skill)

        try:
            # Attempt to increase the skill level
            experience_cost = character_skill.increase_level()
            
            # Display success message
            messages.success(
                request, 
                f"Successfully upgraded {skill.name} to level {character_skill.level}. Cost: {experience_cost} XP."
            )

        except ValidationError as e:
            # Handle errors (e.g., not enough experience or max level reached)
            messages.error(request, str(e))
        
        return redirect("characters:skill_upgrade_list", character_id=character.id)

    context = {
        "character": character,
        "skill_data": skill_data,  # Pass the list of (skill, character_skill) pairs
    }
    return render(request, "characters/skill_upgrade_list.html", context)



@login_required
def create_character(request):
    if request.method == "POST":
        form = CharacterCreationForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.player = request.user
            character.save()
            # Assign role aptitudes to the character
            character.assign_role_aptitudes()
            return redirect("characters:character_detail", character_name=character.name)
    else:
        form = CharacterCreationForm()

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
def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, "characters/campaign_list.html", {
        "campaigns": campaigns,
    })


@login_required
def campaign_detail(request, campaign_name):
    campaign = get_object_or_404(Campaign, name=campaign_name)
    user_characters = Character.objects.filter(player=request.user).exclude(id__in=campaign.characters.values_list('id', flat=True))
    is_master = request.user == campaign.campaign_master

    # Get characters in the campaign excluding the campaign master's character
    campaign_characters = campaign.characters.all()
    master_character = campaign.characters.filter(player=campaign.campaign_master).first()

    # Pending requests (only visible to the campaign master)
    pending_requests = campaign.pending_requests.all() if is_master else None


    if request.method == "POST":
        character_id = request.POST.get("character_id")
        action = request.POST.get("action")
        experience_points = request.POST.get("experience_points")

        # Ensure experience points is a valid integer, defaulting to 0 if not provided
        try:
            experience_points = int(experience_points)
        except (TypeError, ValueError):
            experience_points = 0

        # Handle individual character actions
        if character_id:
            character = get_object_or_404(Character, id=character_id)

            if action == "assign_experience" and is_master:
                # Assign experience to individual character
                campaign.assign_experience(character, experience_points)

            elif action == "request_to_join" and character.player == request.user:
                campaign.request_to_join(character)

            elif is_master:
                if action == "approve_request":
                    campaign.approve_request(character)
                elif action == "decline_request":
                    campaign.decline_request(character)

            # Remove character (either by owner or master)
            if action == "remove_character" and (character.player == request.user or is_master):
                campaign.remove_character(character)

            # Distribute experience to all characters
            if action == "assign_experience_all" and is_master:
                for character in campaign_characters:
                    campaign.assign_experience(character, experience_points)

        return redirect("characters:campaign_detail", campaign_name=campaign.name)

    return render(request, "characters/campaign_detail.html", {
        "campaign": campaign,
        "user_characters": user_characters,
        "campaign_characters": campaign_characters,
        "is_master": is_master,
        "master_character": master_character,
        "pending_requests": pending_requests,
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