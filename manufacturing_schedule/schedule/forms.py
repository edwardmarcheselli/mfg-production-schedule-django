from django import forms
from .models import Release

class CreateRelease(forms.ModelForm):
    class Meta:
        model = Release
        fields = ['bom', 'project', 'requested_completion_date', 'priority']
        widgets = {
            'requested_completion_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }