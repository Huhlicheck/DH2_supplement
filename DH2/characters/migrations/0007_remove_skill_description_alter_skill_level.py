# Generated by Django 5.1.2 on 2024-10-31 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0006_skill_character_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='description',
        ),
        migrations.AlterField(
            model_name='skill',
            name='level',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
