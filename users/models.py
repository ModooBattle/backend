import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Location(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="user_location", blank=False, null=False, help_text="유저pk"
    )
    address = models.CharField(max_length=50, blank=False, null=False, help_text="도로명주소 또는 지번주소")
    latitude = models.FloatField(blank=False, null=False, help_text="위도")
    longitude = models.FloatField(blank=False, null=False, help_text="경도")

    def __str__(self):
        return self.address


class User(AbstractUser):
    ageRegex = RegexValidator(regex=r"^[1-3]{1}[0]{1}$", message="10, 20, 30 가능", code=412)
    genderRegex = RegexValidator(regex=r"^[MF]{1}$", message="M 또는 F, (male or female)", code=412)
    usernameRegex = RegexValidator(regex=r"^[가-힣a-z0-9]{3,15}$", message="한글, 소문자, 숫자만 가능, 3-15자", code=412)

    username = models.CharField(
        validators=[usernameRegex],
        max_length=15,
        unique=True,
        blank=False,
        null=False,
        help_text="닉네임(한글, 소문자, 숫자만 가능, 3-15자)",
    )
    email = models.EmailField(help_text="메일주소", max_length=45, unique=True, blank=False, null=False)
    age = models.CharField(validators=[ageRegex], max_length=2, blank=False, null=False, help_text="연령, 10, 20, 30")
    gender = models.CharField(
        validators=[genderRegex], max_length=1, blank=False, null=False, help_text="성별 M(남), F(여)"
    )
    is_active = models.BooleanField(default=True, blank=True, null=False, help_text="유저 상태(활성화 여부)")
    sport = models.ForeignKey("sports.Sport", on_delete=models.PROTECT, blank=False, null=False, help_text="종목아이디")

    weight = models.ForeignKey("sports.Weight", on_delete=models.PROTECT, blank=False, null=False, help_text="체급아이디")
    years = models.PositiveIntegerField(
        blank=False, null=False, validators=[MinValueValidator(1), MaxValueValidator(10)], help_text="스포츠경력(1-10)"
    )
    gym = models.ForeignKey(
        "sports.Gym", on_delete=models.PROTECT, related_name="users", blank=False, null=False, help_text="체육관아이디"
    )

    yellow_card = models.PositiveIntegerField(default=0, blank=True, null=False, help_text="유효신고횟수")
    uuid = models.UUIDField(default=uuid.uuid4, blank=False, null=False)

    def __str__(self):
        return self.username
