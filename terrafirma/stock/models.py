from django.db import models

from terrafirma.core import models as c_models


class Stock(models.Model):
    pass


class StockAddition(models.Model):
    pass


class StockUsage(models.Model):
    plant = models.ForeignKey(c_models.Plant, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(blank=True)
    unit = models.CharField(max_length=1, choices=c_models.HARVEST_UNITS)
    date = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class StockExpiry(StockUsage):
    def __repr__(self):
        return "Expiry()".format()

    def __str__(self):
        return "expiry".format()

    class Meta:
        verbose_name_plural = 'stock expiries'


class StockRemoval(StockUsage):
    def __repr__(self):
        return "Removal()".format()

    def __str__(self):
        return "removal".format()
