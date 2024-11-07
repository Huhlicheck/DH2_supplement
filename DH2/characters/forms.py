from django.core.exceptions import ValidationError
from django import forms
from .models import Character, Campaign, Characteristic

class CharacterCreationForm(forms.ModelForm):
    characteristic_points = forms.IntegerField(initial=60, required=False, label="Remaining Points", disabled=True)

    class Meta:
        model = Character
        fields = ['name', 'character_homeworld', 'character_background', 'character_role']

    def __init__(self, *args, **kwargs):
        selected_role = kwargs.pop('selected_role', None)  # Get the selected role
        super().__init__(*args, **kwargs)

        if selected_role:
            # Loop over characteristic types to allow user to distribute points
            for index, characteristic_type in enumerate(selected_role.characteristic_types.all()):
                self.fields[f'characteristic_choice_{index}'] = forms.IntegerField(
                    min_value=0,
                    max_value=15,  # Maximum points to allocate for each characteristic
                    label=f"Allocate points to {characteristic_type.name}",
                    initial=0
                )

    def save(self, commit=True):
        character = super().save(commit=False)
        character.character_role = self.cleaned_data['character_role']  # Set the role

        if commit:
            character.save()

            # Allocate points to characteristics
            remaining_points = 60
            for field_name, points in self.cleaned_data.items():
                if field_name.startswith('characteristic_choice_'):
                    characteristic_index = int(field_name.split('_')[-1])
                    characteristic_type = character.character_role.characteristic_types.all()[characteristic_index]
                    
                    # Ensure the points allocated do not exceed the allowed points
                    if points <= remaining_points:
                        characteristic = Characteristic.objects.create(
                            character=character,
                            characteristic_type=characteristic_type,
                            value=characteristic_type.default_value + points
                        )
                        remaining_points -= points
                    else:
                        raise ValidationError("Not enough points allocated for the characteristics.")

            # Update remaining points
            character.characteristic_points = remaining_points
            character.save()

        return character



 

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