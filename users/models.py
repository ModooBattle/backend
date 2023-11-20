from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid

class User(AbstractUser):
    # nicknameRegex = RegexValidator(regex = r'^[가-힣a-zA-Z0-9]{1,20}$', message='한글, 영문, 숫자만 가능, 20자 이내',code=412)
    ageRegex = RegexValidator(regex = r'^[1-0]{1}[0]{1}$', message='10, 20, 30, 40, 50 등의 연령',code=412)
    genderRegex = RegexValidator(regex = r'^[MF]{1}$', message='M 또는 F, (male or female)',code=412)
    
  
    # nickname = models.CharField(validators = [nicknameRegex], max_length=20, unique=True, blank=False, null=False)  #프론트에서 length 검사 필요
    age = models.CharField(validators = [ageRegex], max_length=2, blank=False, null=False)
    gender = models.CharField(validators = [genderRegex], max_length=1, blank=False, null=False)
    is_active = models.BooleanField(default=True, blank=True, null=False)
    yellow_card = models.PositiveIntegerField(default=0, blank=True, null=False)
    uuid = models.UUIDField(default=uuid.uuid4, blank=False, null=False)
    
    def __str__(self):
        return self.nickname
