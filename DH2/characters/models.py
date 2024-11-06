from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError




class Aptitude(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    role_bonus = models.TextField(blank=True, null=True)
    aptitudes = models.ManyToManyField(Aptitude, related_name="roles")

    def __str__(self):
        return self.name   



class Character(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="characters")
    character_homeworld = models.CharField(max_length=255, null=False, blank=False)
    character_background = models.CharField(max_length=255, null=False, blank=False)
    character_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="characters")
    aptitudes = models.ManyToManyField(Aptitude, related_name="characters", blank=True)
    experience_to_spend = models.PositiveIntegerField(default=0)
    experience_total = models.PositiveIntegerField(default=0)
    wounds = models.IntegerField(default=0)
    fatigue = models.IntegerField(default=0)

    class Meta:
        unique_together = ('name', 'player')  # Ensures unique character names per user

    def __str__(self):
        return f"{self.name} ({self.player.username})"

    def assign_role_aptitudes(self):
        """Assigns the aptitudes from the selected role to the character."""
        if self.character_role:
            self.aptitudes.set(self.character_role.aptitudes.all())




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

            
@receiver(post_save, sender=Character)
def add_general_aptitude(sender, instance, created, **kwargs):
    if created:
        general_aptitude, _ = Aptitude.objects.get_or_create(name="General")
        instance.aptitudes.add(general_aptitude)


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    default_level = models.IntegerField(default=-10)  # Starting level for new skills (-10)

    # Each skill has two aptitudes that provide a discount
    primary_aptitude = models.ForeignKey(
        'Aptitude', on_delete=models.SET_NULL, null=True, related_name='primary_skills'
    )
    secondary_aptitude = models.ForeignKey(
        'Aptitude', on_delete=models.SET_NULL, null=True, related_name='secondary_skills'
    )

    def __str__(self):
        return self.name


class CharacterSkill(models.Model):
    LEVEL_COSTS = {
        0: (300, 200, 100),
        10: (600, 400, 200),
        20: (900, 600, 300),
        30: (1200, 800, 400),
    }

    character = models.ForeignKey('Character', on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='character_skills')
    level = models.IntegerField(default=-10)  # Levels: -10, 0, 10, 20, 30

    class Meta:
        unique_together = ('character', 'skill')  # Ensure a unique skill per character

    def __str__(self):
        return f"{self.character}'s {self.skill.name} at level {self.level}"

    def get_upgrade_cost(self):
        """
        Calculate the experience cost for upgrading the skill level based on character's aptitudes.
        """
        next_level = self.level + 10
        if next_level not in CharacterSkill.LEVEL_COSTS:
            raise ValidationError("Maximum skill level reached.")

        # Base cost for moving to the next level
        base_cost, one_aptitude_cost, both_aptitude_cost = CharacterSkill.LEVEL_COSTS[next_level]

        # Check character aptitudes
        aptitudes = self.character.aptitudes.values_list('id', flat=True)
        if (self.skill.primary_aptitude_id in aptitudes) and (self.skill.secondary_aptitude_id in aptitudes):
            return both_aptitude_cost  # Discount if both aptitudes match
        elif (self.skill.primary_aptitude_id in aptitudes) or (self.skill.secondary_aptitude_id in aptitudes):
            return one_aptitude_cost  # Partial discount if one aptitude matches
        return base_cost  # No discount

    def increase_level(self):
        """
        Increase the skill level, if possible, and deduct experience points.
        """
        if self.level >= 30:
            raise ValidationError("Skill is already at maximum level.")
        
        # Calculate the cost
        experience_cost = self.get_upgrade_cost()

        # Check if character has enough experience
        if self.character.experience_to_spend < experience_cost:
            raise ValidationError("Not enough experience points.")

        # Deduct experience points and increase the level
        self.character.experience_to_spend -= experience_cost
        self.level += 10
        self.character.save()
        self.save()
        return experience_cost  # Return the cost for reference





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
        character.experience_to_spend += experience_points
        character.experience_total += experience_points
        character.save()