from rest_framework import serializers
from .models import User

class UserInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username',)
        
class KakaoSerializer(serializers.Serializer):
    code = serializers.CharField() 