# Generated by Django 4.2.6 on 2024-02-12 14:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sports", "0006_alter_gym_latitude_alter_gym_longitude"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gym",
            name="latitude",
            field=models.FloatField(
                help_text="위도",
                validators=[
                    django.core.validators.MinValueValidator(-90.0),
                    django.core.validators.MaxValueValidator(90.0),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="gym",
            name="longitude",
            field=models.FloatField(
                help_text="경도",
                validators=[
                    django.core.validators.MinValueValidator(-180.0),
                    django.core.validators.MaxValueValidator(180.0),
                ],
            ),
        ),
    ]
