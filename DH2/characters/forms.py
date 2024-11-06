from django import forms
from .models import Character, Campaign, Role

class CharacterCreationForm(forms.ModelForm):
    character_role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)

    class Meta:
        model = Character
        fields = ['name', 'character_homeworld', 'character_background', 'character_role']


 

class CampaignCreationForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description']
        labels = {
            'name': 'Campaign Name',
            'description': 'Description',
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Campaign.objects.filter(name=name).exists():
            raise forms.ValidationError("A campaign with this name already exists.")
        return name