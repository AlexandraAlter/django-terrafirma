from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CalendarConfig(AppConfig):
    name = 'terrafirma.calendar'
    label = 'terrafirma_calendar'
    verbose_name = _('Terrafirma Calendar')
