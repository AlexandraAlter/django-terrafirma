from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django import views
from django.views import generic as g_views
from django.views.generic import base as b_views, edit as e_views

from .. import forms, models


class NewEnvView(e_views.CreateView):
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


class EnvView(EnvMixin, g_views.DetailView):
    model = models.Environment
    slug_field = 'abbrev'
    slug_url_kwarg = 'env_abbrev'


class EditEnvView(EnvMixin, e_views.UpdateView):
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
