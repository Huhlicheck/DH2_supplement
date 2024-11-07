from django.contrib import admin

from .models import Character, Item, Campaign, CharacteristicType, Skill, Role

admin.site.register(Character)
admin.site.register(Campaign)
admin.site.register(Item)
admin.site.register(CharacteristicType)
admin.site.register(Skill)
admin.site.register(Role)