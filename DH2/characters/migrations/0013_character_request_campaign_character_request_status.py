# Generated by Django 5.1.2 on 2024-11-03 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0012_campaign_pending_requests'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='request_campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pending_join_requests', to='characters.campaign'),
        ),
        migrations.AddField(
            model_name='character',
            name='request_status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')], default=None, max_length=10, null=True),
        ),
    ]
