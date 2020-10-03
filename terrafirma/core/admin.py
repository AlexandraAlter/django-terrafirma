from django.contrib import admin


from . import models


admin.site.register(models.Note)
admin.site.register(models.Environment)
admin.site.register(models.Bed)
admin.site.register(models.PlantType)
admin.site.register(models.Plant)
admin.site.register(models.Transplanting)
admin.site.register(models.Harvest)
admin.site.register(models.Observation)
admin.site.register(models.TreatmentType)
admin.site.register(models.Treatment)
admin.site.register(models.MaladyType)
admin.site.register(models.Malady)
