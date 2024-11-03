from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




    
    

class Character(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="characters")
    character_homeworld = models.CharField(max_length=255, null=False, blank=False)
    character_background = models.CharField(max_length=255, null=False, blank=False)
    character_class = models.CharField(max_length=255, null=False, blank=False)
    character_aptitudes = models.CharField(max_length=255)
    experience_to_spend = models.PositiveIntegerField(default=0)
    experience_total = models.PositiveIntegerField(default=0)
    wounds = models.IntegerField(default=0)
    fatigue = models.IntegerField(default=0)

    class Meta:
        unique_together = ('name', 'player')  # Ensures unique character names per user

    def __str__(self):
        return f"{self.name} ({self.character_homeworld}, {self.character_background}, {self.character_class})"
    



class AttributeType(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Strength", "Dexterity"
    default_value = models.IntegerField(default=22)  # Default starting value for all characters

    def __str__(self):
        return self.name



class Attribute(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="attributes")
    attribute_type = models.ForeignKey(AttributeType, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.attribute_type.name}: {self.value} (Character: {self.character.name})"




@receiver(post_save, sender=Character)
def create_default_attributes(sender, instance, created, **kwargs):
    if created:
        for attribute_type in AttributeType.objects.all():
            Attribute.objects.create(
                character=instance,
                attribute_type=attribute_type,
                value=attribute_type.default_value
            )


# Keep the base Skill model as a reference for skill types
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    default_level = models.PositiveIntegerField(default=0)  # Default level for new skills

    def __str__(self):
        return self.name


# Create a CharacterSkill model to link each character with specific skill levels
class CharacterSkill(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="character_skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="character_skills")
    level = models.PositiveIntegerField(default=0)  # Level specific to this character

    def __str__(self):
        return f"{self.skill.name} (Level: {self.level}) - {self.character.name}"


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=50)  # e.g., "Weapon", "Armor", "Potion"
    rarity = models.IntegerField(default=0)  # gold value or rarity level

    def __str__(self):
        return self.name




class CharacterItem(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="inventory")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    equipped = models.BooleanField(default=False)

    def __str__(self):
        status = "Equipped" if self.equipped else "In Inventory"
        return f"{self.character.name} - {self.item.name} ({status})"



class Campaign(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    campaign_master = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="mastered_campaigns")
    characters = models.ManyToManyField("Character", related_name="campaigns", blank=True)
    pending_requests = models.ManyToManyField("Character", related_name="pending_campaign_requests", blank=True)

    def __str__(self):
        return self.name

    def add_character(self, character):
        """Adds a character to the campaign, if allowed."""
        if character not in self.characters.all() and character.player != self.campaign_master:
            self.characters.add(character)
    
    def remove_character(self, character):
        """Removes a character from the campaign."""
        if character in self.characters.all():
            self.characters.remove(character)

    def request_to_join(self, character):
        if character not in self.characters.all() and character not in self.pending_requests.all():
            self.pending_requests.add(character)

    def approve_request(self, character):
        if character in self.pending_requests.all():
            self.pending_requests.remove(character)
            self.characters.add(character)

    def decline_request(self, character):
        if character in self.pending_requests.all():
            self.pending_requests.remove(character)

    def assign_experience(self, character, experience_points):
        """Assigns experience points to a character if the user is the campaign master."""
        if character in self.characters.all() and self.campaign_master != character.player:
            character.experience_to_spend += experience_points
            character.experience_total += experience_points
            character.save()