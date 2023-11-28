from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework import exceptions, decorators, permissions, status


from drf_yasg.utils       import swagger_auto_schema
from .serializers import WeightSerializer, WeightQuerySerializer, SportsSerializer
from .models import Weight, Sport
# from .schema import log

swagger_tag = '대결종목'

class SportsListView(APIView) :
    @swagger_auto_schema(tags=[swagger_tag], operation_summary='종목리스트',  responses={200: 'ok'})
    def get(self, request):
        
        try:
            sports_list = Sport.objects.all()
            serializer = SportsSerializer(sports_list, many=True)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except Weight.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data='this sports list does not exist')

class WeightListView(APIView) :
    @swagger_auto_schema(tags=[swagger_tag], operation_summary='체급리스트', query_serializer=WeightQuerySerializer, responses={200: 'ok'})
    def get(self, request):
        
        sport = request.GET['sport_id']
        gender = request.GET['gender']
        try:
            weight_list = Weight.objects.filter(sport=sport, gender=gender)
            serializer = WeightSerializer(weight_list, many=True)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except Weight.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data='this weight list does not exist')
            