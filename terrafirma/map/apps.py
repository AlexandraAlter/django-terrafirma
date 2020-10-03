from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MapConfig(AppConfig):
    name = 'terrafirma.map'
    verbose_name = _('Terrafirma Map')
