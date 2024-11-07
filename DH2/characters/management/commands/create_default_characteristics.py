from django.core.management.base import BaseCommand
from characters.models import CharacteristicType, Aptitude

class Command(BaseCommand):
    help = "Create default characteristics and associate aptitudes"

    def handle(self, *args, **kwargs):
        # List of characteristic names and their associated aptitudes
        characteristics_data = {
            "Weapon Skill": ["Weapon Skill", "Offence"],
            "Ballistic Skill": ["Ballistic Skill", "Finesse"],
            "Strength": ["Strength", "Offence"],
            "Toughness": ["Toughness", "Defence"],
            "Agility": ["Agility", "Finesse"],
            "Intelligence": ["Intelligence", "Knowledge"],
            "Perception": ["Perception", "Fieldcraft"],
            "Willpower": ["Willpower", "Psyker"],
            "Fellowship": ["Fellowship", "Social"]
        }

        # Create the characteristics and associate the aptitudes
        for characteristic_name, aptitude_names in characteristics_data.items():
            # Create the CharacteristicType (if not already exists)
            characteristic_type, created = CharacteristicType.objects.get_or_create(
                name=characteristic_name, default_value=20
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created characteristic: {characteristic_name}"))

            # Create and associate the aptitudes
            for aptitude_name in aptitude_names:
                aptitude, _ = Aptitude.objects.get_or_create(name=aptitude_name)
                characteristic_type.aptitudes.add(aptitude)

            self.stdout.write(self.style.SUCCESS(f"Associated aptitudes for {characteristic_name}: {', '.join(aptitude_names)}"))

        self.stdout.write(self.style.SUCCESS("Default characteristics and aptitudes created successfully."))
