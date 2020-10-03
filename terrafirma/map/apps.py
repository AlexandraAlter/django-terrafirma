from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MapConfig(AppConfig):
    name = 'terrafirma.map'
    label = 'terrafirma_map'
    verbose_name = _('Terrafirma Map')
