# Generated by Django 3.1.2 on 2020-10-03 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terrafirma', '0002_auto_20201003_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='TreatmentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='bed',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='bed',
            name='environment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='terrafirma.environment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bed',
            name='name',
            field=models.CharField(default=None, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bed',
            name='short_name',
            field=models.CharField(default=None, max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='environment',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='environment',
            name='short_name',
            field=models.CharField(default=None, max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sowing',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sowing',
            name='number',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sowing',
            name='unit',
            field=models.CharField(choices=[('s', 'seeds'), ('r', 'rows')], default=None, max_length=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='TreatmentInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('bed', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terrafirma.bed')),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terrafirma.treatment')),
            ],
        ),
        migrations.AddField(
            model_name='treatment',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terrafirma.treatmenttype'),
        ),
        migrations.CreateModel(
            name='Transplanting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('bed', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terrafirma.bed')),
                ('sowing', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terrafirma.sowing')),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sowing', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terrafirma.sowing')),
            ],
        ),
        migrations.CreateModel(
            name='Harvesting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sowing', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terrafirma.sowing')),
            ],
        ),
    ]
