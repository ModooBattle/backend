from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid


class Weight(models.Model):
    genderRegex = RegexValidator(regex = r'^[MF]{1}$', message='M 또는 F, (male or female)',code=412)
    
    sport_name = models.CharField(validators = [genderRegex], max_length=1, blank=False, null=False)
    gender = models.CharField(validators = [genderRegex], max_length=1, blank=False, null=False)
    min_weight = models.PositiveIntegerField(blank=False, null=False)
    max_weight = models.PositiveIntegerField(blank=False, null=False)
    
class MyAddress(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='my_addr', blank=False, null=False)
    address_name = models.CharField(max_length=150, blank=False, null=False)
    latitude = models.IntegerField(blank=False, null=False)
    longitude = models.IntegerField(blank=False, null=False)
    
class GymAddress(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='gym_addr', blank=False, null=False)
    address_name = models.CharField(max_length=150, blank=False, null=False)
    latitude = models.IntegerField(blank=False, null=False)
    longitude = models.IntegerField(blank=False, null=False)
     

class User(AbstractUser):
    # nicknameRegex = RegexValidator(regex = r'^[가-힣a-zA-Z0-9]{1,20}$', message='한글, 영문, 숫자만 가능, 20자 이내',code=412)
    ageRegex = RegexValidator(regex = r'^[1-3]{1}[0]{1}$', message='10, 20, 30 가능',code=412)
    genderRegex = RegexValidator(regex = r'^[MF]{1}$', message='M 또는 F, (male or female)',code=412)
    usernameRegex = RegexValidator(regex = r'^[가-힣a-z0-9]{5,15}$', message='한글, 소문자, 숫자만 가능, 5-15자',code=412)
    
    
    # nickname = models.CharField(validators = [nicknameRegex], max_length=20, unique=True, blank=False, null=False)  #프론트에서 length 검사 필요
    username = models.CharField(validators = [usernameRegex], max_length=15, unique=True, blank=False, null=False)
    age = models.CharField(validators = [ageRegex], max_length=2, blank=False, null=False)
    gender = models.CharField(validators = [genderRegex], max_length=1, blank=False, null=False)
    is_active = models.BooleanField(default=True, blank=True, null=False)
    weight = models.ForeignKey('users.Weight', on_delete=models.PROTECT, null=True)
    yellow_card = models.PositiveIntegerField(default=0, blank=True, null=False)
    kakao_id = models.CharField(max_length=50, blank=False, null=False)
    uuid = models.UUIDField(default=uuid.uuid4, blank=False, null=False)
    
    def __str__(self):
        return self.username
    

