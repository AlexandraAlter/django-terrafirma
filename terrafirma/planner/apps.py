from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlannerConfig(AppConfig):
    name = 'terrafirma.planner'
    label = 'terrafirma_planner'
    verbose_name = _('Terrafirma Planner')
