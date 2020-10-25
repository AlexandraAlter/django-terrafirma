from django.shortcuts import redirect
from django import views
from django.views import generic as g_views
from django.views.generic import base as b_views, edit as e_views

from .. import forms, models
from .plant import PlantMixin

# observations


class NewPlantObsView(PlantMixin, e_views.CreateView):
    model = models.Observation
    form_class = forms.ObsForm
    template_name_suffix = '_plant_form'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.note = models.Note(text=form.cleaned_data['note'])
        self.object.note.save()
        self.object.plant = self.plant
        self.object.save()
        return redirect('plant', plant_id=self.plant.id)


# treatment types


class TreatmentTypeListView(g_views.ListView):
    model = models.TreatmentType


class NewTreatmentTypeView(e_views.CreateView):
    model = models.TreatmentType
    fields = ['name', 'type']


class TreatmentTypeView(g_views.DetailView):
    model = models.TreatmentType
    slug_field = 'id'
    slug_url_kwarg = 'trt_type_id'


# treatments


class NewPlantTrtView(NewPlantObsView):
    model = models.Treatment
    form_class = forms.TrtForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('plant', plant_id=plant.id)


# malady types


class MaladyTypeListView(g_views.ListView):
    model = models.MaladyType


class NewMaladyTypeView(e_views.CreateView):
    model = models.MaladyType
    fields = ['name', 'type']


class MaladyTypeView(g_views.DetailView):
    model = models.MaladyType
    slug_field = 'id'
    slug_url_kwarg = 'mal_type_id'


# maladies


class NewPlantMalView(NewPlantObsView):
    model = models.Malady
    form_class = forms.MalForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('plant', plant_id=plant.id)
