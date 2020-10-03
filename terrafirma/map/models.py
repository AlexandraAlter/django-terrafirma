from django.db import models

from terrafirma.core import models as c_models


class Map(models.Model):
    environment = models.ForeignKey(c_models.Environment,
                                    on_delete=models.PROTECT,
                                    blank=True,
                                    null=True)
    pixels_x = models.PositiveIntegerField()
    pixels_y = models.PositiveIntegerField()
    spec = models.JSONField()

    def __repr__(self):
        return "Map".format()

    def __str__(self):
        return "map".format()
