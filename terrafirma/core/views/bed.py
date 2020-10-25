from django.shortcuts import render, redirect, get_object_or_404
from django import views
from django.views.generic import base as b_views, edit as e_views

from .. import forms, models
from .env import EnvMixin, MaybeEnvMixin

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
