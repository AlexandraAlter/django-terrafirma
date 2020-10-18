from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django import views
from django.views.generic import base as b_views, edit as e_views
from django.db import transaction

from . import forms, models


class HomeView(views.View):
    def get(self, request, *args, **kwargs):
        env_list = models.Environment.objects.all()
        orph = models.Plant.objects.without_bed().all
        return render(request, 'terrafirma/home.html', {'env_list': env_list, 'orphaned': orph})


# plant types


class PlantTypeListView(views.View):
    def get(self, request, *args, **kwargs):
        plant_types = models.PlantType.objects.all()
        return render(request, 'terrafirma/plant_types.html', {'plant_types': plant_types})


class PlantTypeView(views.View):
    def get(self, request, *args, **kwargs):
        plant_type = models.PlantType.objects.get(id=kwargs.get('plant_type_id'))
        plantings = models.Plant.objects.filter(type=plant_type)
        observations = None
        return render(request, 'terrafirma/plant_type.html', {
            'plant_type': plant_type,
            'plantings': plantings,
            'observations': observations,
        })


class NewPlantTypeView(e_views.CreateView):
    template_name = 'terrafirma/new_plant_type.html'
    model = models.PlantType
    fields = ['common_name', 'variety']

    def form_valid(self, form):
        form.save()
        return redirect('plant-types')


# environments


class NewEnvView(e_views.CreateView):
    template_name = 'terrafirma/new_env.html'
    model = models.Environment
    fields = ['name', 'abbrev']
    success_url = reverse_lazy('home')


class EnvMixin(b_views.ContextMixin):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.env = get_object_or_404(models.Environment, abbrev=kwargs['env_abbrev'])

    def url_vars(self):
        return {'env_abbrev': self.env.abbrev}

    def get_context_data(self, **kwargs):
        return super().get_context_data(env=self.env, **kwargs)


class MaybeEnvMixin(b_views.ContextMixin):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.env = models.Environment.objects.get(abbrev=request.GET['env'])

    def url_vars(self):
        return {'env_abbrev': self.env.abbrev if self.env else None}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.env:
            context.update(env=self.env)
        return context


class EnvView(EnvMixin, views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'terrafirma/env.html', {'env': self.env})


class EditEnvView(EnvMixin, e_views.UpdateView):
    template_name = 'terrafirma/edit_env.html'
    model = models.Environment
    fields = ['name', 'abbrev']
    slug_field = 'abbrev'
    slug_url_kwarg = 'env_abbrev'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object = self.env

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('env', env_abbrev=self.env.abbrev)


# beds


class NewBedView(EnvMixin, e_views.CreateView):
    template_name = 'terrafirma/new_bed.html'
    model = models.Bed
    fields = ['name', 'abbrev']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.env = self.env
        self.object.save()
        return redirect('env', env_abbrev=self.env.abbrev)


class BedMixin(EnvMixin):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.bed = get_object_or_404(models.Bed, abbrev=kwargs['bed_abbrev'], env=self.env)
        # TODO make this more efficient instead of getting every class above
        # self.env = self.bed.env

    def url_vars(self):
        return {'env_abbrev': self.env.abbrev, 'bed_abbrev': self.bed.abbrev}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(bed=self.bed, **kwargs)
        return context


class MaybeBedMixin(MaybeEnvMixin):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.bed = models.Bed.objects.get(abbrev=request.GET['bed'], env=self.env)

    def url_vars(self):
        vars = super().url_vars()
        vars.update({'bed_abbrev': self.bed.abbrev if self.bed else None})
        return vars

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.bed:
            context.update(bed=self.bed)
        return context


class BedListView(views.View):
    def get(self, request, *args, **kwargs):
        beds = models.Bed.objects.all()
        return render(request, 'terrafirma/beds.html', {'beds': beds})


class BedView(BedMixin, views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'terrafirma/bed.html', {'env': self.env, 'bed': self.bed})


class EditBedView(BedMixin, e_views.UpdateView):
    template_name = 'terrafirma/edit_bed.html'
    model = models.Bed
    fields = ['name', 'abbrev']
    slug_field = 'abbrev'
    slug_url_kwarg = 'bed_abbrev'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object = self.bed

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('bed', env_abbrev=self.env.abbrev, bed_abbrev=self.bed.abbrev)


# plants


class PlantListView(views.View):
    def get(self, request, *args, **kwargs):
        plants = models.Plant.objects.all()
        return render(request, 'terrafirma/plants.html', {'plants': plants})


class NewPlantView(MaybeBedMixin, e_views.CreateView):
    template_name = 'terrafirma/new_plant.html'
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


class PlantView(PlantMixin, views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'terrafirma/plant.html', {
            'plant': self.plant,
        })


class EditPlantView(PlantMixin, e_views.UpdateView):
    template_name = 'terrafirma/edit_plant.html'
    model = models.Plant
    fields = ['type', 'amount', 'unit']
    slug_field = 'id'
    slug_url_kwarg = 'plant_id'

    def form_valid(self, form):
        plant = form.save()
        return redirect('plant', **self.url_vars())


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


class NewPlantTrtView(NewPlantObsView):
    model = models.Treatment
    form_class = forms.TrtForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('plant', plant_id=plant.id)


class NewPlantMalView(NewPlantObsView):
    model = models.Malady
    form_class = forms.MalForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('plant', plant_id=plant.id)
