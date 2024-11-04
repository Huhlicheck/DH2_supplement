from django.core.management.base import BaseCommand
from characters.models import Aptitude

class Command(BaseCommand):
    help = "Create default aptitudes for characters"

    def handle(self, *args, **kwargs):
        aptitudes = [
            "General", "Weapon Skill", "Ballistic Skill", "Strength", "Toughness", 
            "Agility", "Intelligence", "Perception", "Willpower", "Fellowship",
            "Offence", "Finesse", "Defence", "Psyker", "Tech", "Knowledge", 
            "Leadership", "Fieldcraft", "Social"
        ]

        for aptitude_name in aptitudes:
            aptitude, created = Aptitude.objects.get_or_create(name=aptitude_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created aptitude: {aptitude_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Aptitude already exists: {aptitude_name}"))
