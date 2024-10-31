# Generated by Django 5.1.2 on 2024-10-30 21:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0002_alter_character_fatigue_alter_character_wounds'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('default_value', models.IntegerField(default=22)),
            ],
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='name',
        ),
        migrations.AlterField(
            model_name='attribute',
            name='value',
            field=models.IntegerField(),
        ),
        migrations.AddField(
            model_name='attribute',
            name='attribute_type',
            field=models.ForeignKey(default=22, on_delete=django.db.models.deletion.CASCADE, to='characters.attributetype'),
            preserve_default=False,
        ),
    ]