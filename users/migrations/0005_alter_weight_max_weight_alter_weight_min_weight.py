# Generated by Django 4.2.6 on 2023-11-28 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_weight_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="weight",
            name="max_weight",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="weight",
            name="min_weight",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]