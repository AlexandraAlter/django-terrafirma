from django.db import models


class Stock(models.Model):
    pass

class StockUsage(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(blank=True)
    unit = models.CharField(max_length=1, choices=HARVEST_UNITS)
    date = models.DateField(auto_now=True)


class Sale(StockUsage):
    value = models.DecimalField(max_digits=8, decimal_places=2)

    def __repr__(self):
        return "Sale()".format()

    def __str__(self):
        return "sale".format()


class A(StockUsage):

    def __repr__(self):
        return "Nom()".format()

    def __str__(self):
        return "nom".format()


class Expiry(StockUsage):

    def __repr__(self):
        return "Nom()".format()

    def __str__(self):
        return "nom".format()
