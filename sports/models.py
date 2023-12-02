from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length=15, unique=True, blank=False, null=False)


class Weight(models.Model):
    genderRegex = RegexValidator(
        regex=r"^[MF]{1}$", message="M 또는 F, (male or female)", code=412
    )

    name = models.CharField(max_length=15, blank=False, null=False)
    sport = models.ForeignKey("sports.Sport", on_delete=models.PROTECT, null=False)
    gender = models.CharField(
        validators=[genderRegex],
        max_length=1,
        blank=False,
        null=False,
        help_text="남성 M, 여성 F",
    )
    min_weight = models.PositiveIntegerField(blank=False, null=False)


class Gym(models.Model):
    sport = models.ForeignKey("sports.Sport", on_delete=models.PROTECT, null=False)
    name = models.CharField(max_length=15, blank=False, null=False)
    address = models.CharField(max_length=50, blank=False, null=False)
    latitude = models.IntegerField(blank=False, null=False)
    longitude = models.IntegerField(blank=False, null=False)
