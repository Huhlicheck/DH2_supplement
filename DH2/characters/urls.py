from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.custom_login_view, name='login'),
    path("", views.character_list, name="character_list"),
    path("<str:character_name>/", views.character_detail, name="character_detail"),
]