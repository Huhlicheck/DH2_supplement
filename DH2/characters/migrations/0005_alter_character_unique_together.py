# Generated by Django 5.1.2 on 2024-10-30 22:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0004_rename_experience_points_character_experience_to_spend_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='character',
            unique_together={('name', 'player')},
        ),
    ]
