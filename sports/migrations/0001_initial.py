# Generated by Django 4.2.6 on 2023-11-28 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Sport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name="Gym",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=15)),
                ("address", models.CharField(max_length=50)),
                ("latitude", models.IntegerField()),
                ("longitude", models.IntegerField()),
                (
                    "sport",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="sports.sport"
                    ),
                ),
            ],
        ),
    ]
