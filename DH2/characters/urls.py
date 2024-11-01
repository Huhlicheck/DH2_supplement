from django.urls import path

from . import views

app_name = "characters"
urlpatterns = [
    path("", views.character_list, name="character_list"),
    path("<str:character_name>/", views.character_detail, name="character_detail"),
    path('campaign/<str:campaign_name>/', views.campaign_detail, name='campaign_detail'),
]