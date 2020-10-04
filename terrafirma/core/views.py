from django.shortcuts import render, redirect
from django import views

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


class EnvView(views.View):
    def get(self, request, *args, **kwargs):
        env = models.Environment.objects.get(name=kwargs.get('env_name'))
        return render(request, 'terrafirma/env.html', {'env': env})
