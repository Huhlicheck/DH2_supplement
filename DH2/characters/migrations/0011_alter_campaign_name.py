# Generated by Django 5.1.2 on 2024-11-01 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0010_campaign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]