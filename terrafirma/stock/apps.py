from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StockConfig(AppConfig):
    name = 'terrafirma.stock'
    label = 'terrafirma_stock'
    verbose_name = _('Terrafirma Stock')
