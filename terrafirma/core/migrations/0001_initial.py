# Generated by Django 3.1.2 on 2020-10-18 22:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('abbrev', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('^[a-z\\-0-9]+\\Z', 'Only use lowercase a-z, numbers, and hyphens.')], verbose_name='abbreviation')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('abbrev', models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator('^[a-z\\-0-9]+\\Z', 'Only use lowercase a-z, numbers, and hyphens.')], verbose_name='abbreviation')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaladyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('type', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('unit', models.CharField(choices=[('s', 'seeds'), ('r', 'rows')], default='s', max_length=1)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlantType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name', models.CharField(max_length=64)),
                ('variety', models.CharField(max_length=64)),
            ],
            options={
                'unique_together': {('common_name', 'variety')},
            },
        ),
        migrations.CreateModel(
            name='TreatmentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('type', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(default=django.utils.timezone.now)),
                ('bed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.bed')),
                ('env', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.environment', verbose_name='environment')),
                ('note', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.note')),
                ('plant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.plant')),
                ('plant_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.planttype')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terrafirma.treatmenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transplanting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('bed', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transplants', to='terrafirma.bed')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transplants', to='terrafirma.plant')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddField(
            model_name='plant',
            name='beds',
            field=models.ManyToManyField(through='terrafirma.Transplanting', to='terrafirma.Bed'),
        ),
        migrations.AddField(
            model_name='plant',
            name='cur_transplant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='terrafirma.transplanting'),
        ),
        migrations.AddField(
            model_name='plant',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terrafirma.planttype'),
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(default=django.utils.timezone.now)),
                ('bed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.bed')),
                ('env', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.environment', verbose_name='environment')),
                ('note', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.note')),
                ('plant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.plant')),
                ('plant_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.planttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Malady',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(default=django.utils.timezone.now)),
                ('bed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.bed')),
                ('env', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.environment', verbose_name='environment')),
                ('note', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.note')),
                ('plant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.plant')),
                ('plant_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.planttype')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terrafirma.maladytype')),
            ],
            options={
                'verbose_name_plural': 'maladies',
            },
        ),
        migrations.CreateModel(
            name='Harvest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(blank=True)),
                ('unit', models.CharField(choices=[('g', 'grams'), ('c', 'count')], max_length=1)),
                ('in_stock', models.BooleanField(default=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terrafirma.plant')),
            ],
        ),
        migrations.AddField(
            model_name='bed',
            name='env',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='beds', to='terrafirma.environment', verbose_name='environment'),
        ),
        migrations.AddConstraint(
            model_name='transplanting',
            constraint=models.UniqueConstraint(condition=models.Q(active=True), fields=('plant',), name='unique_active'),
        ),
        migrations.AlterUniqueTogether(
            name='bed',
            unique_together={('name', 'env'), ('abbrev', 'env')},
        ),
    ]
