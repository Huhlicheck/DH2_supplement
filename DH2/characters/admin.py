from django.contrib import admin

from .models import Character, Item, Campaign, Aptitude, Skill

admin.site.register(Character)
admin.site.register(Campaign)
admin.site.register(Item)
admin.site.register(Aptitude)
admin.site.register(Skill)