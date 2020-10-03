from django.contrib import admin


from . import models


admin.site.register(models.PlantType)
admin.site.register(models.Environment)
admin.site.register(models.Bed)
admin.site.register(models.Treatment)
admin.site.register(models.TreatmentInstance)
admin.site.register(models.Malady)
admin.site.register(models.MaladyInstance)
admin.site.register(models.Plant)
admin.site.register(models.Transplanting)
admin.site.register(models.Harvest)
admin.site.register(models.Observation)
