from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length=15, unique=True, blank=False, null=False, help_text="스포츠명")

    def __str__(self):
        return self.name


class Weight(models.Model):
    genderRegex = RegexValidator(regex=r"^[MF]{1}$", message="M 또는 F, (male or female)", code=412)

    name = models.CharField(max_length=15, blank=False, null=False, help_text="체급명")
    sport = models.ForeignKey("sports.Sport", on_delete=models.PROTECT, null=False, help_text="종목아이디")
    gender = models.CharField(validators=[genderRegex], max_length=1, blank=False, null=False, help_text="남성 M, 여성 F")
    min_weight = models.PositiveIntegerField(blank=False, null=False, help_text="해당몸무게(kg) 이상")

    def __str__(self):
        return f"{self.sport}/{self.gender}/{self.name}"


class Gym(models.Model):
    sport = models.ForeignKey("sports.Sport", on_delete=models.PROTECT, null=False, help_text="종목아이디")
    name = models.CharField(max_length=15, blank=False, null=False, help_text="체육관이름")
    address = models.CharField(max_length=50, blank=False, null=False, help_text="도로명주소 또는 지번주소")
    latitude = models.FloatField(
        blank=False,
        null=False,
        validators=[MinValueValidator(-90.000000), MaxValueValidator(90.000000)],
        help_text="위도",
    )
    longitude = models.FloatField(
        blank=False,
        null=False,
        validators=[MinValueValidator(-180.000000), MaxValueValidator(180.000000)],
        help_text="경도",
    )

    def __str__(self):
        return f"{self.sport}/{self.name}/{self.address}"
