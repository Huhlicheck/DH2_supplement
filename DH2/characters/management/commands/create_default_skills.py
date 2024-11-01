from django.core.management.base import BaseCommand
from characters.models import Skill

class Command(BaseCommand):
    help = "Create default skills for all characters"

    def handle(self, *args, **kwargs):
        skills = ["Athletics","Logic","Medicae"]
        for skill in skills:
            Skill.objects.get_or_create(name=skill, default_value=0)
        self.stdout.write(self.style.SUCCESS("Default skills created successfully."))
