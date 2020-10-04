from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django import views
from django.views.generic import edit as e_views

from . import forms, models


class HomeView(views.View):
    def get(self, request, *args, **kwargs):
        env_list = models.Environment.objects.all()
        return render(request, 'terrafirma/home.html', {'env_list': env_list})


class NewEnvironmentView(views.View):
    def get(self, request, *args, **kwargs):
        form = forms.EnvForm()
        return render(request, 'terrafirma/new_env.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.EnvForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'terrafirma/new_env.html', {'form': form})


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


class NewPlantTypeView(views.View):
    def get(self, request, *args, **kwargs):
        form = forms.PlantTypeForm()
        return render(request, 'terrafirma/new_plant_type.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.PlantTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plants')
        else:
            return render(request, 'terrafirma/new_plant_type.html', {'form': form})


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


# environments


class EnvView(views.View):
    def get(self, request, *args, **kwargs):
        env = get_object_or_404(models.Environment, name=kwargs['env_name'])
        return render(request, 'terrafirma/env.html', {'env': env, 'beds': env.beds.all()})


class NewBedView(e_views.CreateView):
    template_name = 'terrafirma/new_bed.html'
    model = models.Bed
    fields = ['name', 'long_name']

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.env = get_object_or_404(models.Environment, name=kwargs['env_name'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['env'] = self.env
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.environment = self.env
        self.object.save()
        return redirect('env', env_name=self.env.name)


class EditBedView(NewBedView):
    def get(self, request, *args, **kwargs):
        env = get_object_or_404(models.Environment, name=kwargs['env_name'])
        form = forms.BedForm()
        return render(request, 'terrafirma/new_bed.html', {'env': env, 'form': form})

    def post(self, request, *args, **kwargs):
        env = get_object_or_404(models.Environment, name=kwargs['env_name'])
        bed = models.Bed(environment=env)
        form = forms.BedForm(request.POST, instance=bed)
        if form.is_valid():
            form.save()
            return redirect('env', env_name=env.name)
        else:
            return render(request, 'terrafirma/new_bed.html', {'env': env, 'form': form})


class BedListView(views.View):
    def get(self, request, *args, **kwargs):
        beds = models.Bed.objects.all()
        return render(request, 'terrafirma/beds.html', {'beds': beds})


class BedView(views.View):
    def get(self, request, *args, **kwargs):
        bed = models.Bed.objects.get(name=kwargs.get('bed_name'))
        return render(request, 'terrafirma/bed.html', {'bed': bed})
