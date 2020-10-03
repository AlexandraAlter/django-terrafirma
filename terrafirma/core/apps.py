from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = 'terrafirma.core'
    label = 'terrafirma'
    verbose_name = _('Terrafirma Core')
