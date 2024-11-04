from django.core.management.base import BaseCommand
from characters.models import Aptitude, Skill

class Command(BaseCommand):
    help = "Create default skills for all characters"

    def handle(self, *args, **kwargs):          # Define skills and their matching aptitudes
        skills_data = [
            {"name": "Acrobatics", "aptitude_1": "Agility", "aptitude_2": "General"},
            {"name": "Athletics", "aptitude_1": "Strength", "aptitude_2": "General"},
            {"name": "Awareness", "aptitude_1": "Perception", "aptitude_2": "Fieldcraft"},
            {"name": "Charm", "aptitude_1": "Fellowship", "aptitude_2": "Social"},
            {"name": "Command", "aptitude_1": "Fellowship", "aptitude_2": "Leadership"},
            {"name": "Commerce", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Common Lore (Administratum)", "aptitude_1": "Intelligence", "aptitude_2": "General"},
            {"name": "Common Lore (Adeptus Mechanicum)", "aptitude_1": "Intelligence", "aptitude_2": "General"},
            {"name": "Common Lore (Calixis Sector)", "aptitude_1": "Intelligence", "aptitude_2": "General"},
            {"name": "Common Lore (Ecclesiarchy)", "aptitude_1": "Intelligence", "aptitude_2": "General"},
            {"name": "Common Lore (Imperium)", "aptitude_1": "Intelligence", "aptitude_2": "General"},
            {"name": "Common Lore (Imperial Guard)", "aptitude_1": "Intelligence", "aptitude_2": "General"},
            {"name": "Common Lore (Underworld)", "aptitude_1": "Intelligence", "aptitude_2": "General"},
            {"name": "Common Lore (War)", "aptitude_1": "Intelligence", "aptitude_2": "General"},
            {"name": "Common Lore (Tech)", "aptitude_1": "Intelligence", "aptitude_2": "General"},
            {"name": "Deceive", "aptitude_1": "Fellowship", "aptitude_2": "Social"},
            {"name": "Dodge", "aptitude_1": "Agility", "aptitude_2": "Defence"},
            {"name": "Forbidden Lore (Archaeotech)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Forbidden Lore (Daemonology)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Forbidden Lore (Mutants)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Forbidden Lore (Warp)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Forbidden Lore (Heresy)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Forbidden Lore (Xenos)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Inquiry", "aptitude_1": "Fellowship", "aptitude_2": "Social"},
            {"name": "Interrogation", "aptitude_1": "Willpower", "aptitude_2": "Social"},
            {"name": "Intimidate", "aptitude_1": "Strength", "aptitude_2": "Social"},
            {"name": "Linguistics", "aptitude_1": "Intelligence", "aptitude_2": "General"},
            {"name": "Logic", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Medicae", "aptitude_1": "Intelligence", "aptitude_2": "Fieldcraft"},
            {"name": "Navigate (Surface)", "aptitude_1": "Intelligence", "aptitude_2": "Fieldcraft"},
            {"name": "Navigate (Stellar)", "aptitude_1": "Intelligence", "aptitude_2": "Fieldcraft"},
            {"name": "Navigate (Warp)", "aptitude_1": "Intelligence", "aptitude_2": "Fieldcraft"},        
            {"name": "Operate", "aptitude_1": "Agility", "aptitude_2": "Fieldcraft"},
            {"name": "Parry", "aptitude_1": "Weapon Skill", "aptitude_2": "Defence"},
            {"name": "Psyniscience", "aptitude_1": "Perception", "aptitude_2": "Psyker"},
            {"name": "Scholastic Lore (Occult)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Scholastic Lore (Judgement)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Scholastic Lore (Chymistry)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Scholastic Lore (Imperial Creed)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Scholastic Lore (Numerology)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Scholastic Lore (Philosophy)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Scholastic Lore (Tactica Imperialis)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Scholastic Lore (Heraldry)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Scholastic Lore (Astromancy)", "aptitude_1": "Intelligence", "aptitude_2": "Knowledge"},
            {"name": "Scrutiny", "aptitude_1": "Perception", "aptitude_2": "General"},
            {"name": "Security", "aptitude_1": "Intelligence", "aptitude_2": "Tech"},
            {"name": "Sleight of Hand", "aptitude_1": "Agility", "aptitude_2": "Knowledge"},
            {"name": "Stealth", "aptitude_1": "Agility", "aptitude_2": "Fieldcraft"},
            {"name": "Survival", "aptitude_1": "Perception", "aptitude_2": "Fieldcraft"},
            {"name": "Tech-Use", "aptitude_1": "Intelligence", "aptitude_2": "Tech"},
            {"name": "Trade", "aptitude_1": "Intelligence", "aptitude_2": "General"},
        ]


        # Create skills with aptitudes
        for skill_data in skills_data:
            aptitude_1 = Aptitude.objects.get(name=skill_data["aptitude_1"])
            aptitude_2 = Aptitude.objects.get(name=skill_data["aptitude_2"])

            skill, created = Skill.objects.get_or_create(
                name=skill_data["name"],
                defaults={
                    "primary_aptitude": aptitude_1,
                    "secondary_aptitude": aptitude_2,
                    "default_level": -10,  # Default starting level
                },
            )

            if created:
                print(f"Created skill: {skill.name} with aptitudes {aptitude_1} and {aptitude_2}")
            else:
                print(f"Skill already exists: {skill.name}")