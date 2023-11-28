from rest_framework import serializers
from .models import Weight, Sport

class WeightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Weight
        fields = ('id', 'name', 'min_weight')


class WeightQuerySerializer(serializers.ModelSerializer):
    sport_id = serializers.IntegerField(source='sport', help_text='경기종목 id')
        
    class Meta:
        model = Weight
        fields = ('sport_id', 'gender')
        
class SportsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sport
        fields = ('id', 'name',)
