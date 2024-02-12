# Generated by Django 4.2.6 on 2024-02-12 14:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0023_rename_userlocation_location"),
    ]

    operations = [
        migrations.CreateModel(
            name="BannedUser",
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
                (
                    "email",
                    models.EmailField(help_text="메일주소", max_length=45, unique=True),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="작성일", null=True),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="location",
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
            model_name="location",
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
