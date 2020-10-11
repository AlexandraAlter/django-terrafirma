from django.db import models
from django.db.models import functions, Q, Subquery
from django.urls import reverse
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

UNIT_SEEDS = 's'
UNIT_ROWS = 'r'
UNIT_G = 'g'
UNIT_COUNT = 'c'
PLANTING_UNITS = [(UNIT_SEEDS, 'seeds'), (UNIT_ROWS, 'rows')]
HARVEST_UNITS = [(UNIT_G, 'grams'), (UNIT_COUNT, 'count')]

short_name_validator = RegexValidator(r'^[a-z\-0-9]+\Z',
                                      _('Only use lowercase a-z, numbers, and hyphens.'))


class Note(models.Model):
    text = models.TextField(blank=True)
    text_md5 = models.CharField(max_length=32, default=functions.MD5('text'))

    def __repr__(self):
        return "PlantType({}, {})".format(self.common_name, self.variety)

    def __str__(self):
        return "char[{}]".format(len(self.text))


class Environment(models.Model):
    name = models.CharField(max_length=64, unique=True)
    abbrev = models.CharField(max_length=16,
                              unique=True,
                              validators=[short_name_validator],
                              verbose_name=_('abbreviation'))
    active = models.BooleanField(default=True)

    def __repr__(self):
        return "Environment({}, {}, {})".format(self.abbrev, self.name, self.active)

    def __str__(self):
        return self.__format__('')

    def __format__(self, format):
        active = '' if self.active else 'inactive '
        if format == 'longnameonly':
            return "{}{}".format(active, self.name)
        else:
            return "{}{} ({})".format(active, self.name, self.abbrev)

    def get_absolute_url(self):
        return reverse('env', kwargs={'env_abbrev': self.abbrev})


class Bed(models.Model):
    name = models.CharField(max_length=64)
    abbrev = models.CharField(max_length=16,
                              validators=[short_name_validator],
                              verbose_name=_('abbreviation'))
    env = models.ForeignKey(Environment,
                            on_delete=models.PROTECT,
                            related_name='beds',
                            verbose_name=_('environment'))
    active = models.BooleanField(default=True)

    @property
    def cur_plants(self):
        return Plant.objects.filter(transplants__bed=self, transplants__active=True).all()

    def __repr__(self):
        return "Bed({}, {}, {}, active={})".format(self.abbrev, self.name, self.env, self.active)

    def __str__(self):
        return self.__format__('')

    def __format__(self, format):
        active = '' if self.active else 'inactive '
        if format == 'nameonly':
            return "{}{} ({})".format(active, self.name, self.abbrev)
        elif format == 'longnameonly':
            return "{}{}".format(active, self.name)
        else:
            return "{}{} ({}) in {}".format(active, self.name, self.abbrev, self.env.name)

    def get_absolute_url(self):
        return reverse('bed', kwargs={'env_abbrev': self.env.abbrev, 'bed_abbrev': self.abbrev})

    class Meta:
        unique_together = [('abbrev', 'env'), ('name', 'env')]


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

    def get_absolute_url(self):
        return reverse('plant-type', kwargs={'plant_type_id': self.id})

    class Meta:
        unique_together = [('common_name', 'variety')]


def validate_transplant_current(transplant):
    return transplant.active


class PlantManager(models.Manager):
    def without_bed(self):
        transplants = Transplanting.objects.filter(active=True).all()
        return self.exclude(id__in=Subquery(transplants.values('plant')))


class Plant(models.Model):
    type = models.ForeignKey(PlantType, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    unit = models.CharField(max_length=1, choices=PLANTING_UNITS)
    active = models.BooleanField(default=True)
    cur_transplant = models.ForeignKey('Transplanting',
                                       on_delete=models.PROTECT,
                                       related_name='+',
                                       blank=True,
                                       null=True)
    beds = models.ManyToManyField(Bed, through='Transplanting')

    objects = PlantManager()

    @property
    def cur_bed(self):
        return self.cur_transplant.bed

    def __repr__(self):
        return "Plant({}, {}, {}, active={})".format(self.type, self.amount, self.unit, self.active)

    def __str__(self):
        active = '' if self.active else 'dead '
        return "{}plant {}, {} {}".format(active, self.type, self.amount, self.get_unit_display())

    def get_absolute_url(self):
        bed = self.cur_bed
        return reverse('plant',
                       kwargs={
                           'env_abbrev': bed.env.abbrev,
                           'bed_abbrev': bed.abbrev,
                           'plant_id': self.id
                       })

    def clean(self):
        # current transplant is active and refers to this plant
        if self.cur_transplant:
            if not self.cur_transplant.active:
                raise ValidationError(_('Plants current transplant cannot be inactive.'))
            if self.cur_transplant.plant != self:
                raise ValidationError(_('Plants current transplant must self-refer.'))


class Transplanting(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.PROTECT, related_name='transplants')
    date = models.DateTimeField(default=timezone.now)
    bed = models.ForeignKey(Bed, on_delete=models.PROTECT, related_name='transplants')
    active = models.BooleanField(default=True)

    def __repr__(self):
        return "Transplanting({}, {}, {})".format(self.plant, self.date, self.bed)

    def __str__(self):
        active = 'current' if self.active else 'past'
        return "{} transplanting {} {} {}".format(active, self.plant, self.date, self.bed)

    class Meta:
        constraints = [
            # one active transplant per plant
            models.UniqueConstraint(fields=['plant'],
                                    condition=Q(active=True),
                                    name='unique_active')
        ]
        ordering = ['-date']


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
    env = models.ForeignKey(Environment,
                            on_delete=models.PROTECT,
                            blank=True,
                            null=True,
                            verbose_name=_('environment'))

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
