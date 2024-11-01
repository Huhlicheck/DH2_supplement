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
