from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django import views
from django.views.generic import edit as e_views

from . import forms, models


class HomeView(views.View):
    def get(self, request, *args, **kwargs):
        env_list = models.Environment.objects.all()
        return render(request, 'terrafirma/home.html', {'env_list': env_list})


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


# plants


class PlantListView(views.View):
    def get(self, request, *args, **kwargs):
        plants = models.Plant.objects.all()
        return render(request, 'terrafirma/plants.html', {'plants': plants})


class PlantView(views.View):
    def get(self, request, *args, **kwargs):
        plant = models.Plant.objects.get(id=kwargs.get('plant_id'))
        return render(request, 'terrafirma/plant.html', {
            'plant': plant,
        })


class NewPlantView(views.View):
    def get(self, request, *args, **kwargs):
        form = forms.PlantForm()
        return render(request, 'terrafirma/new_plant.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.PlantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plants')
        else:
            return render(request, 'terrafirma/new_plant.html', {'form': form})


# transplants


class NewTransplantView(views.View):
    def get(self, request, *args, **kwargs):
        plant = get_object_or_404(models.Plant, id=kwargs['plant_id'])
        form = forms.TransplantForm(initial={'plant': plant})
        return render(request, 'terrafirma/new_transplant.html', {'plant': plant, 'form': form})

    def post(self, request, *args, **kwargs):
        plant = get_object_or_404(models.Plant, id=kwargs['plant_id'])
        form = forms.TransplantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plants')
        else:
            return render(request, 'terrafirma/new_transplant.html', {'plant': plant, 'form': form})


class NewTransplantView(e_views.CreateView):
    template_name = 'terrafirma/new_transplant.html'
    model = models.Transplanting
    fields = ['bed']

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.plant = get_object_or_404(models.Plant, id=kwargs['plant_id'])

    def get_context_data(self, **kwargs):
        return super().get_context_data(plant=self.plant, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('plant', plant_id=self.plant.id)


# environments


class EnvView(views.View):
    def get(self, request, *args, **kwargs):
        env = get_object_or_404(models.Environment, name=kwargs['env_name'])
        return render(request, 'terrafirma/env.html', {'env': env, 'beds': env.beds.all()})


class NewEnvironmentView(e_views.CreateView):
    template_name = 'terrafirma/new_env.html'
    model = models.Environment
    fields = ['name', 'long_name']
    success_url = reverse_lazy('home')


# beds


class BedListView(views.View):
    def get(self, request, *args, **kwargs):
        beds = models.Bed.objects.all()
        return render(request, 'terrafirma/beds.html', {'beds': beds})


class BedView(views.View):
    def get(self, request, *args, **kwargs):
        env = get_object_or_404(models.Environment, name=kwargs['env_name'])
        bed = get_object_or_404(models.Bed, name=kwargs['bed_name'])
        return render(request, 'terrafirma/bed.html', {'env': env, 'bed': bed})


class NewBedView(e_views.CreateView):
    template_name = 'terrafirma/new_bed.html'
    model = models.Bed
    fields = ['name', 'long_name']

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.env = get_object_or_404(models.Environment, name=kwargs['env_name'])

    def get_context_data(self, **kwargs):
        return super().get_context_data(env=self.env, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.environment = self.env
        self.object.save()
        return redirect('env', env_name=self.env.name)


class EditBedView(e_views.UpdateView):
    template_name = 'terrafirma/edit_bed.html'
    model = models.Bed
    fields = ['name', 'long_name']
    slug_field = 'name'
    slug_url_kwarg = 'bed_name'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object = get_object_or_404(models.Bed, name=kwargs['bed_name'])
        self.env = get_object_or_404(models.Environment, name=kwargs['env_name'])
        self.bed = self.object

    def get_context_data(self, **kwargs):
        return super().get_context_data(env=self.env, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('bed', env_name=self.env.name, bed_name=self.bed.name)
