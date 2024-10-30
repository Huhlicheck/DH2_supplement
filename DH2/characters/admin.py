from django.contrib import admin

from .models import Character, Attribute, AttributeType, Item, CharacterItem

admin.site.register(Character)
admin.site.register(Attribute)
admin.site.register(AttributeType)
admin.site.register(Item)
admin.site.register(CharacterItem)