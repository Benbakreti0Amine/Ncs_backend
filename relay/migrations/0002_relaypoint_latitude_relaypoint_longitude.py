# Generated by Django 5.0.6 on 2025-06-30 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relay', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='relaypoint',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='relaypoint',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
