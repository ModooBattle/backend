# Generated by Django 4.2.6 on 2023-12-29 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sports", "0005_alter_gym_address_alter_gym_latitude_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gym",
            name="latitude",
            field=models.FloatField(help_text="위도"),
        ),
        migrations.AlterField(
            model_name="gym",
            name="longitude",
            field=models.FloatField(help_text="경도"),
        ),
    ]
