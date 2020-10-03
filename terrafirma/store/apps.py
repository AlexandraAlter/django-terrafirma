from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StoreConfig(AppConfig):
    name = 'terrafirma.store'
    label = 'terrafirma_store'
    verbose_name = _('Terrafirma Store')
