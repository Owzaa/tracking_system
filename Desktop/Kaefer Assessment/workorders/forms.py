from django import forms
from .models import ScaffoldComponent
from django.core.exceptions import ValidationError

class ScaffoldComponentForm(forms.ModelForm):
    class Meta:
        model = ScaffoldComponent
        fields = '__all__'
        # Exclude fields that are auto-set or not meant for direct user input
        exclude = ['created_at', 'updated_at'] 
        widgets = {
            'last_inspection': forms.DateInput(attrs={'type': 'date'}),
            'next_inspection': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_weight_kg(self):
        weight_kg = self.cleaned_data['weight_kg']
        if weight_kg <= 0:
            raise ValidationError('Weight (kg) must be greater than 0.')
        return weight_kg

    def clean_length_mm(self):
        length_mm = self.cleaned_data['length_mm']
        if length_mm is not None and not (1 <= length_mm <= 6000):
            raise ValidationError('Length (mm) must be between 1 and 6000.')
        return length_mm

    def clean(self):
        cleaned_data = super().clean()
        last_inspection = cleaned_data.get('last_inspection')
        next_inspection = cleaned_data.get('next_inspection')
        asset_code = cleaned_data.get('asset_code')
        site = cleaned_data.get('site')

        if last_inspection and next_inspection and next_inspection < last_inspection:
            self.add_error('next_inspection', 'Next inspection date must be on or after the last inspection date.')
        
        # Enforce unique together (asset_code, site) with a user-friendly error
        if asset_code and site and self.instance.pk is None: # Only for creation
            if ScaffoldComponent.objects.filter(asset_code=asset_code, site=site).exists():
                self.add_error('asset_code', 'An asset with this code already exists at this site.')
        elif asset_code and site and self.instance.pk is not None: # For update
            if ScaffoldComponent.objects.filter(asset_code=asset_code, site=site).exclude(pk=self.instance.pk).exists():
                self.add_error('asset_code', 'An asset with this code already exists at this site.')
        
        return cleaned_data
