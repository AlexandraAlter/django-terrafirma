from django.db import models

from terrafirma.stock import models as s_models


class StoreSale(s_models.StockUsage):
    value = models.DecimalField(max_digits=8, decimal_places=2)

    def __repr__(self):
        return "Sale()".format()

    def __str__(self):
        return "sale".format()
