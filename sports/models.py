from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length=15, unique=True, blank=False, null=False, help_text="스포츠명")


class Weight(models.Model):
    genderRegex = RegexValidator(regex=r"^[MF]{1}$", message="M 또는 F, (male or female)", code=412)

    name = models.CharField(max_length=15, blank=False, null=False, help_text="체급명")
    sport = models.ForeignKey("sports.Sport", on_delete=models.PROTECT, null=False, help_text="종목아이디")
    gender = models.CharField(validators=[genderRegex], max_length=1, blank=False, null=False, help_text="남성 M, 여성 F")
    min_weight = models.PositiveIntegerField(blank=False, null=False, help_text="해당몸무게(kg) 이상")


class Gym(models.Model):
    sport = models.ForeignKey("sports.Sport", on_delete=models.PROTECT, null=False, help_text="종목아이디")
    name = models.CharField(max_length=15, blank=False, null=False, help_text="체육관이름")
    address = models.CharField(max_length=50, blank=False, null=False, help_text="도로명주소 또는 지번주소")
    latitude = models.IntegerField(blank=False, null=False, help_text="위도")
    longitude = models.IntegerField(blank=False, null=False, help_text="경도")
