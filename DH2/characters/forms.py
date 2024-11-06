from django import forms
from .models import Character, Campaign, Role

class CharacterCreationForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True, label="Select Role")

    class Meta:
        model = Character
        fields = ['name', 'character_homeworld', 'character_background']

    # Dynamically add fields based on available aptitude choices
    def __init__(self, *args, **kwargs):
        selected_role = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)

        if selected_role:
            # Iterate over aptitude choices
            for index, aptitude_choices in enumerate(selected_role.aptitudes.all()):
                if len(aptitude_choices) > 1:
                    # If multiple aptitudes, create a choice field
                    self.fields[f'aptitude_choice_{index}'] = forms.ChoiceField(
                        choices=[(apt.name, apt.name) for apt in aptitude_choices],
                        label=f"Choose aptitude ({' or '.join([apt.name for apt in aptitude_choices])})"
                    )

 

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