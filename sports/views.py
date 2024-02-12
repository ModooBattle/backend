from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, exceptions, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Location
from users.serializers import UserGymListSerializer

from .models import Gym, Sport, Weight
from .serializers import (
    SportsSerializer,
    UserGymListQuerySerializer,
    WeightQuerySerializer,
    WeightSerializer,
)

# from .schema import log

swagger_tag = "대결종목"


class SportsListView(APIView):
    @swagger_auto_schema(tags=[swagger_tag], operation_summary="종목리스트", responses={200: "ok"})
    def get(self, request):
        try:
            sports_list = Sport.objects.all()
            serializer = SportsSerializer(sports_list, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Weight.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="this sports list does not exist")


class WeightListView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="체급리스트",
        query_serializer=WeightQuerySerializer,
        responses={200: "ok"},
    )
    def get(self, request):
        sport = request.GET["sport_id"]
        gender = request.GET["gender"]
        try:
            weight_list = Weight.objects.filter(sport=sport, gender=gender)
            serializer = WeightSerializer(weight_list, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Weight.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="this weight list does not exist")


@decorators.permission_classes([permissions.IsAuthenticated])
class GymListView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="체육관리스트 조회 및 검색",
        query_serializer=UserGymListQuerySerializer,
        responses={200: "ok", 401: "unauthorized"},
    )
    def get(self, request):
        distance_limit = int(request.GET["distance_limit"])
        page_no = int(request.GET["page_no"])
        length = int(request.GET["length"])
        search_category = request.GET.get("search_category", None)
        search_value = request.GET.get("search_value", None)

        start = length * (page_no - 1)

        user_id = request.user.id

        sport_id = request.user.sport_id

        try:
            current_location = Location.objects.get(user=user_id)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Current location required")

        try:
            if search_category and search_value:
                if search_category == "name":
                    gym_list = Gym.objects.raw(
                        f"SELECT *, ROUND(ST_Distance_Sphere(POINT({current_location.longitude},{current_location.latitude}), POINT(longitude,latitude))/1000,1) AS distance FROM sports_gym HAVING distance <= {distance_limit} AND sport_id = {sport_id} AND name LIKE '%%{search_value}%%' ORDER BY distance ASC LIMIT {start}, {length}"
                    )

                elif search_category == "address":
                    gym_list = Gym.objects.raw(
                        f"SELECT *, ROUND(ST_Distance_Sphere(POINT({current_location.longitude},{current_location.latitude}), POINT(longitude,latitude))/1000,1) AS distance FROM sports_gym HAVING distance <= {distance_limit} AND sport_id = {sport_id} AND address LIKE '%%{search_value}%%' ORDER BY distance ASC LIMIT {start}, {length}"
                    )

                else:
                    return Response(
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        data="search_category : name or address",
                    )
            else:
                gym_list = Gym.objects.raw(
                    f"""SELECT *, ROUND(ST_Distance_Sphere(POINT({current_location.longitude},{current_location.latitude}), POINT(longitude,latitude))/1000,1) AS distance FROM sports_gym HAVING distance <= {distance_limit} AND sport_id = {sport_id} ORDER BY distance ASC LIMIT {start}, {length}"""
                )

            serializer = UserGymListSerializer(gym_list, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Weight.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="this weight list does not exist")
