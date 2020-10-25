from .env import *
from .bed import *
from .plant import *
from .obs import *

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django import views

from .. import forms, models


class HomeView(views.View):
    def get(self, request, *args, **kwargs):
        context = {
            'env_list': models.Environment.objects.all(),
            'orphaned': models.Plant.objects.without_bed().all,
            'num_plants_alive': models.Plant.objects.filter(active=True).count(),
            'num_plants_dead': models.Plant.objects.filter(active=False).count(),
            'num_plant_types': models.PlantType.objects.count(),
            'num_trt_types': models.Treatment.objects.count(),
            'num_mal_types': models.Malady.objects.count(),
        }
        return render(request, 'terrafirma/home.html', context)
