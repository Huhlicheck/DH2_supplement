from django.core.management.base import BaseCommand, CommandError
from characters.models import Character, Skill

class Command(BaseCommand):
    help = "Assigns skills to a specified character by name."

    def add_arguments(self, parser):
        parser.add_argument('character_name', type=str, help='Name of the character to assign skills to')
        parser.add_argument('--skills', nargs='+', type=str, help='List of skill names to assign', required=True)

    def handle(self, *args, **options):
        character_name = options['character_name']
        skill_names = options['skills']

        # Find the character by name
        try:
            character = Character.objects.get(name=character_name)
            self.stdout.write(self.style.SUCCESS(f"Character '{character_name}' found."))
        except Character.DoesNotExist:
            raise CommandError(f"Character '{character_name}' does not exist.")

        # Add each skill to the character
        for skill_name in skill_names:
            skill, created = Skill.objects.get_or_create(name=skill_name, defaults={'description': 'Default description'})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created new skill '{skill_name}'."))
            character.skills.add(skill)
            self.stdout.write(self.style.SUCCESS(f"Assigned skill '{skill_name}' to '{character_name}'."))

        self.stdout.write(self.style.SUCCESS(f"Successfully assigned skills to character '{character_name}'."))
