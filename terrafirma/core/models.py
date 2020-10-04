from django.db import models
from django.db.models import functions

UNIT_SEEDS = 's'
UNIT_ROWS = 'r'
UNIT_G = 'g'
UNIT_COUNT = 'c'
PLANTING_UNITS = [(UNIT_SEEDS, 'seeds'), (UNIT_ROWS, 'rows')]
HARVEST_UNITS = [(UNIT_G, 'grams'), (UNIT_COUNT, 'count')]


class Note(models.Model):
    text = models.TextField(blank=True)
    text_md5 = models.CharField(max_length=32, default=functions.MD5('text'))

    def __repr__(self):
        return "PlantType({}, {})".format(self.common_name, self.variety)

    def __str__(self):
        return "char[{}]".format(len(self.text))


class Environment(models.Model):
    name = models.CharField(max_length=16)
    long_name = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

    def __repr__(self):
        return "Environment({}, {}, {})".format(self.name, self.long_name, self.active)

    def __str__(self):
        if self.active:
            return "{} ({})".format(self.name, self.long_name)
        else:
            return "inactive {} ({})".format(self.name, self.long_name)


class Bed(models.Model):
    name = models.CharField(max_length=16)
    long_name = models.CharField(max_length=64)
    environment = models.ForeignKey(Environment, on_delete=models.PROTECT, related_name='beds')
    active = models.BooleanField(default=True)

    def __repr__(self):
        return "Bed({}, {}, {}, active={})".format(self.name, self.long_name, self.environment,
                                                   self.active)

    def __str__(self):
        if self.active:
            return "{} {}".format(self.environment.name, self.name)
        else:
            return "inactive {} {}".format(self.environment.name, self.name)


class PlantType(models.Model):
    common_name = models.CharField(max_length=64)
    variety = models.CharField(max_length=64)

    @property
    def full_name(self):
        return "{} {}".format(self.common_name, self.variety)


    def __repr__(self):
        return "PlantType({}, {})".format(self.common_name, self.variety)

    def __str__(self):
        return "{} {}".format(self.common_name, self.variety)


class Plant(models.Model):
    type = models.ForeignKey(PlantType, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    unit = models.CharField(max_length=1, choices=PLANTING_UNITS)
    active = models.BooleanField(default=True)

    @property
    def transplants(self):
        return []

    def __repr__(self):
        return "Plant({}, {}, {}, active={})".format(self.type, self.amount, self.unit, self.active)

    def __str__(self):
        if self.active:
            return "plant {}, {} {}".format(self.type, self.amount, self.get_unit_display())
        else:
            return "dead plant {}, {}{}".format(self.type, self.amount, self.unit)


class Transplanting(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.PROTECT)
    date = models.DateField(auto_now=True)
    bed = models.ForeignKey(Bed, on_delete=models.PROTECT)

    def __repr__(self):
        return "Transplanting({}, {}, {})".format(self.plant, self.date, self.bed)

    def __str__(self):
        return "transplanting {} {} {}".format(self.plant, self.date, self.bed)


class Harvest(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(blank=True)
    unit = models.CharField(max_length=1, choices=HARVEST_UNITS)
    in_stock = models.BooleanField(default=True)

    def __repr__(self):
        return "Harvest()".format()

    def __str__(self):
        return "harvest".format()


class Observation(models.Model):
    plant_type = models.ForeignKey(PlantType, on_delete=models.PROTECT, blank=True, null=True)
    plant = models.ForeignKey(Plant, on_delete=models.PROTECT, blank=True, null=True)
    bed = models.ForeignKey(Bed, on_delete=models.PROTECT, blank=True, null=True)
    environment = models.ForeignKey(Environment, on_delete=models.PROTECT, blank=True, null=True)

    date = models.DateField(auto_now=True)

    text = models.ForeignKey(Note, on_delete=models.PROTECT, blank=True)

    def __repr__(self):
        return "Observation()".format()

    def __str__(self):
        return "observation".format()


class TreatmentType(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64, blank=True)

    def __repr__(self):
        return "TreatmentType({}, {})".format(self.name, self.type)

    def __str__(self):
        return "treatment type {} {}".format(self.type, self.name)


class Treatment(Observation):
    type = models.ForeignKey(TreatmentType, on_delete=models.PROTECT)

    def __repr__(self):
        return "Treatment({}, {}, {}, data=char[{}])".format(self.treatment, self.date, self.bed,
                                                             len(self.details))

    def __str__(self):
        return "treatment {} on {} in {} (char[{}])".format(self.treatment.name, self.date,
                                                            self.bed, len(self.details))


class MaladyType(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64, blank=True)

    def __repr__(self):
        return "MaladyType({}, {})".format(self.name, self.type)

    def __str__(self):
        return "malady type {} {}".format(self.type.name, self.name)


class Malady(models.Model):
    malady = models.ForeignKey(MaladyType, on_delete=models.PROTECT)
    date = models.DateField(auto_now=True)
    bed = models.ForeignKey(Bed, on_delete=models.PROTECT)
    sowing = models.ForeignKey(Plant, on_delete=models.PROTECT)
    details = models.ForeignKey(Note, on_delete=models.PROTECT, blank=True)

    def __repr__(self):
        return "Malady({}, {}, {})".format(self.malady, self.date, self.bed)

    def __str__(self):
        return "malady {} on {} in {}".format(self.malady, self.date, self.bed)

    class Meta:
        verbose_name_plural = 'maladies'
