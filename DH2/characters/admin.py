from django.contrib import admin

from .models import Character, Item, Campaign

admin.site.register(Character)
admin.site.register(Campaign)
admin.site.register(Item)