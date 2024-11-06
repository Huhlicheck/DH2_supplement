from django import forms
from .models import Character, Campaign, Role, Aptitude

class CharacterCreationForm(forms.ModelForm):
    character_role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True, label="Select Role")

    class Meta:
        model = Character
        fields = ['name', 'character_homeworld', 'character_background', 'character_role']  # Use 'character_role' here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        selected_role = self.initial.get('role')
        
        if selected_role:
            # Iterate over aptitude choices
            for index, aptitude_choices in enumerate(selected_role.aptitudes.all()):
                if aptitude_choices.count() > 1:
                    # If multiple aptitudes, create a choice field
                    self.fields[f'aptitude_choice_{index}'] = forms.ChoiceField(
                        choices=[(apt.id, apt.name) for apt in aptitude_choices],
                        label=f"Choose aptitude ({' or '.join([apt.name for apt in aptitude_choices])})"
                    )

    def save(self, commit=True):
        character = super().save(commit=False)
        character.character_role = self.cleaned_data['character_role']  # Use 'character_role' here

        if commit:
            character.save()
            # Assign selected aptitudes to character after saving
            for field_name, aptitude_id in self.cleaned_data.items():
                if field_name.startswith('aptitude_choice_') and aptitude_id:
                    aptitude = Aptitude.objects.get(id=aptitude_id)
                    character.aptitudes.add(aptitude)

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