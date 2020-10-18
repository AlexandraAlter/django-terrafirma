# Generated by Django 3.1.2 on 2020-10-18 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('terrafirma', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(blank=True)),
                ('unit', models.CharField(choices=[('g', 'grams'), ('c', 'count')], max_length=1)),
                ('date', models.DateField(auto_now=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terrafirma.plant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
