from django.core.management.base import BaseCommand
from characters.models import AttributeType

class Command(BaseCommand):
    help = "Create default attributes for all characters"

    def handle(self, *args, **kwargs):
        attributes = ["Weapon Skill","Balistic Skill","Strength","Toughness","Agility", "Intelligence", "Perception", "Willpower", "Fellowship"]
        for attr in attributes:
            AttributeType.objects.get_or_create(name=attr, default_value=22)
        self.stdout.write(self.style.SUCCESS("Default attributes created successfully."))
