from rest_framework import serializers

from .models import Location, User


class LocationRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ["user"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class NicknameQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class UserSerializer(serializers.ModelSerializer):
    location = LocationRegisterSerializer()

    class Meta:
        model = User
        fields = ("username", "age", "gender", "years", "email", "weight", "location")


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "age",
            "gender",
            "years",
            "email",
            "weight",
        )


class KakaoSerializer(serializers.Serializer):
    code = serializers.CharField()
