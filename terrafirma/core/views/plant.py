from django.shortcuts import render, redirect, get_object_or_404
from django import views
from django.views import generic as g_views
from django.views.generic import base as b_views, edit as e_views
from django.db import transaction

from .. import forms, models
from .bed import BedMixin, MaybeBedMixin

# plant types


class PlantTypeListView(g_views.ListView):
    model = models.PlantType


class PlantTypeView(g_views.DetailView):
    model = models.PlantType
    slug_field = 'id'
    slug_url_kwarg = 'plant_type_id'


class NewPlantTypeView(e_views.CreateView):
    model = models.PlantType
    fields = ['common_name', 'variety']

    def form_valid(self, form):
        form.save()
        return redirect('plant-types')


# plants


class PlantListView(g_views.ListView):
    model = models.Plant


class NewPlantView(MaybeBedMixin, e_views.CreateView):
    model = models.Plant
    form_class = forms.PlantForm

    def get_initial(self):
        return {'bed': self.bed} if self.bed else {}

    def form_valid(self, form):
        plant = form.save(commit=False)
        transplant = models.Transplanting(plant=plant, bed=form.cleaned_data.bed)
        with transaction.atomic():
            plant.save()
            transplant.save()
            plant.cur_transplant = transplant
            plant.save()
        form.save_m2m()
        return redirect('bed', **self.url_vars())


class PlantMixin(b_views.ContextMixin):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.plant = get_object_or_404(models.Plant, id=kwargs['plant_id'])

    def url_vars(self):
        return {'plant_id': self.plant.id}

    def get_context_data(self, **kwargs):
        return super().get_context_data(plant=self.plant, **kwargs)


class PlantView(PlantMixin, g_views.DetailView):
    model = models.Plant
    slug_field = 'id'
    slug_url_kwarg = 'plant_id'


class EditPlantView(PlantMixin, e_views.UpdateView):
    template_name_suffix = '_edit_form'
    model = models.Plant
    fields = ['type', 'amount', 'unit']
    slug_field = 'id'
    slug_url_kwarg = 'plant_id'


# transplants


class NewTransplantView(PlantMixin, e_views.CreateView):
    template_name = 'terrafirma/new_transplant.html'
    model = models.Transplanting
    fields = ['bed']

    @transaction.atomic
    def form_valid(self, form):
        transplant = form.save(commit=False)
        transplant.plant = self.plant
        old_transplant = self.plant.cur_transplant
        old_transplant.active = False
        transplant.active = True
        old_transplant.save()
        transplant.save()
        return redirect('plant', plant_id=transplant.plant.id)
