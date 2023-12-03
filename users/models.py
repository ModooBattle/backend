import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Location(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, blank=False, null=False, help_text="사용자아이디")
    address = models.CharField(max_length=50, blank=False, null=False, help_text="도로명주소 또는 지번주소")
    latitude = models.IntegerField(blank=False, null=False, help_text="위도")
    longitude = models.IntegerField(blank=False, null=False, help_text="경도")


class User(AbstractUser):
    # nicknameRegex = RegexValidator(regex = r'^[가-힣a-zA-Z0-9]{1,20}$', message='한글, 영문, 숫자만 가능, 20자 이내',code=412)
    ageRegex = RegexValidator(regex=r"^[1-3]{1}[0]{1}$", message="10, 20, 30 가능", code=412)
    genderRegex = RegexValidator(regex=r"^[MF]{1}$", message="M 또는 F, (male or female)", code=412)
    usernameRegex = RegexValidator(regex=r"^[가-힣a-z0-9]{3,15}$", message="한글, 소문자, 숫자만 가능, 5-15자", code=412)

    # nickname = models.CharField(validators = [nicknameRegex], max_length=20, unique=True, blank=False, null=False)  #프론트에서 length 검사 필요
    username = models.CharField(
        validators=[usernameRegex], help_text="닉네임", max_length=15, unique=True, blank=False, null=False
    )
    age = models.CharField(validators=[ageRegex], max_length=2, blank=False, null=False, help_text="연령")
    gender = models.CharField(validators=[genderRegex], max_length=1, blank=False, null=False, help_text="성별")
    is_active = models.BooleanField(default=True, blank=True, null=False, help_text="유저 상태(활성화 여부)")
    weight = models.ForeignKey("sports.Weight", on_delete=models.PROTECT, null=True, help_text="체급아이디")
    years = models.PositiveIntegerField(
        blank=False, null=False, validators=[MinValueValidator(1), MaxValueValidator(50)], help_text="스포츠경력"
    )
    gym = models.ForeignKey("sports.Gym", on_delete=models.PROTECT, null=True, help_text="체육관아이디")
    yellow_card = models.PositiveIntegerField(default=0, blank=True, null=False, help_text="유효신고횟수")
    # kakao_id = models.CharField(max_length=50, blank=False, null=False)
    uuid = models.UUIDField(default=uuid.uuid4, blank=False, null=False)

    def __str__(self):
        return self.username
