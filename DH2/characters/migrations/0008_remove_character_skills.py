# Generated by Django 5.1.2 on 2024-10-31 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0007_remove_skill_description_alter_skill_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='skills',
        ),
    ]