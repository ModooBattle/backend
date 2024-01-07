from rest_framework import serializers

from sports.models import Gym
from sports.serializers import GymSerializer, WeightSerializer

from .models import Location, User


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class NicknameQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class UserInfoSerializer(serializers.ModelSerializer):
    weight = WeightSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "weight", "age", "gender", "years", "last_login")


class UserSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    gym = GymSerializer()

    class Meta:
        model = User
        fields = ("username", "age", "gender", "years", "email", "weight", "location", "gym")


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "age", "gender", "sport", "years", "email", "weight", "gym")


class KakaoSerializer(serializers.Serializer):
    code = serializers.CharField()


class UserGymListSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField(method_name="get_attributes_sorted")
    distance = serializers.FloatField()

    class Meta:
        model = Gym
        fields = ("id", "name", "address", "distance", "users")

    @staticmethod
    def get_attributes_sorted(instance):
        users = instance.users.order_by("-last_login")
        return UserInfoSerializer(users, many=True).data
