# Generated by Django 5.1.2 on 2024-11-04 20:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0014_remove_character_request_campaign_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aptitude',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RenameField(
            model_name='character',
            old_name='character_class',
            new_name='character_role',
        ),
        migrations.RemoveField(
            model_name='character',
            name='character_aptitudes',
        ),
        migrations.AddField(
            model_name='skill',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='characterskill',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='characters.character'),
        ),
        migrations.AlterField(
            model_name='characterskill',
            name='level',
            field=models.IntegerField(default=-10),
        ),
        migrations.AlterField(
            model_name='skill',
            name='default_level',
            field=models.IntegerField(default=-10),
        ),
        migrations.AlterUniqueTogether(
            name='characterskill',
            unique_together={('character', 'skill')},
        ),
        migrations.AddField(
            model_name='character',
            name='aptitudes',
            field=models.ManyToManyField(blank=True, related_name='characters', to='characters.aptitude'),
        ),
        migrations.AddField(
            model_name='skill',
            name='primary_aptitude',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_skills', to='characters.aptitude'),
        ),
        migrations.AddField(
            model_name='skill',
            name='secondary_aptitude',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secondary_skills', to='characters.aptitude'),
        ),
    ]