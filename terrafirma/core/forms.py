from django import forms
from django.utils.safestring import mark_safe

from . import models


class PlantForm(forms.ModelForm):
    bed = forms.ModelChoiceField(queryset=models.Bed.objects.all())

    class Meta:
        model = models.Plant
        fields = ['type', 'amount', 'unit']
        widgets = {
            'unit': forms.RadioSelect(attrs={'class': 'unit_widget'}, choices=models.PLANTING_UNITS)
        }

    class Media:
        css = {'all': ('terrafirma/css/inline_unit_widget.css', )}


class ObsForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = models.Observation
        fields = ['when']


class TrtForm(ObsForm):
    class Meta(ObsForm.Meta):
        model = models.Treatment
        fields = ['type', 'when']


class MalForm(ObsForm):
    class Meta(ObsForm.Meta):
        model = models.Malady
        fields = ['type', 'when']
