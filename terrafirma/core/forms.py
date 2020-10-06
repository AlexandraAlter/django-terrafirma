from django import forms

from . import models


class EnvForm(forms.ModelForm):
    class Meta:
        model = models.Environment
        exclude = ['active']


class PlantForm(forms.ModelForm):
    class Meta:
        model = models.Plant
        exclude = ['active']


class TransplantForm(forms.ModelForm):
    class Meta:
        model = models.Transplanting
        fields = ['bed']
