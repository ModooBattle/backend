from rest_framework import serializers

from sports.serializers import GymSerializer

from .models import Location, User


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class NicknameQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class UserSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    gym = GymSerializer()

    class Meta:
        model = User
        fields = ("username", "age", "gender", "years", "email", "weight", "location", "gym")


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "age", "gender", "years", "email", "weight", "gym", "current_location")


class KakaoSerializer(serializers.Serializer):
    code = serializers.CharField()
