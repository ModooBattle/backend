from rest_framework import serializers

from .models import Gym, Sport, Weight


class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ("id", "name", "min_weight")


class WeightQuerySerializer(serializers.ModelSerializer):
    sport_id = serializers.IntegerField(source="sport", help_text="경기종목 id")

    class Meta:
        model = Weight
        fields = ("sport_id", "gender")


class UserGymListQuerySerializer(serializers.Serializer):
    distance_limit = serializers.IntegerField(help_text="거리km 이하")
    page_no = serializers.IntegerField(help_text="페이지 No")
    length = serializers.IntegerField(help_text="페이지 당 데이터 수")
    search_category = serializers.CharField(
        required=False, max_length=20, help_text="검색 카테고리: name(체육관명), address(지번주소)"
    )
    search_value = serializers.CharField(required=False, max_length=20, help_text="검색 내용")


class SportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = (
            "id",
            "name",
        )


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = "__all__"
