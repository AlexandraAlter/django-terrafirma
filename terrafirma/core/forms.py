from django import forms

from . import models

class EnvForm(forms.ModelForm):
    class Meta:
        model = models.Environment
        fields = ['name', 'short_name']
