from django.urls import path

from . import views

app_name = "characters"
urlpatterns = [
    path("index/", views.character_list, name="character_list"),
    path("about/", views.about, name="about"),    
    path("contact/", views.contact, name="contact"),
    path("create/", views.create_character, name="create_character"),
    path("delete/<str:character_name>/", views.delete_character, name="delete_character"),
    path('campaigns/', views.campaign_list, name="campaign_list"),
    path("campaign/create/", views.create_campaign, name="create_campaign"),
    path("campaign/delete/<str:campaign_name>/", views.delete_campaign, name="delete_campaign"),
    path('campaign/<str:campaign_name>/', views.campaign_detail, name='campaign_detail'),
    path("<str:character_name>/", views.character_detail, name="character_detail"),
    path('<int:character_id>/skill_upgrade_list/', views.skill_upgrade_list, name='skill_upgrade_list'),
]