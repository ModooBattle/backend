from . import serializers
import requests
from .models import User
from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework import exceptions, decorators, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
from config import settings
from django.utils import timezone
from django.http import Http404

from datetime import datetime, timedelta

from django.db import transaction

from django.core.cache import cache

from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi    
from .serializers import KakaoSerializer 
from .schema import login_res_schema

def get_tokens_for_user(user):
    
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
def login(user):

    tokens = get_tokens_for_user(user)
    res = Response()
    serializer = serializers.UserInfoSerializer(user)
   
    res.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
        value=tokens["refresh"],
        expires=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    res.data = {"tokens":tokens, "user":serializer.data}  
    
    res.status=status.HTTP_200_OK
    
    # WebsocketConnect(user.id)
    
    return res

def kakao_access(request):
 
    serializer = serializers.KakaoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    auth_code = serializer.validated_data["code"]
    
    kakao_token_api = 'https://kauth.kakao.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.KAKAO_REST_API_KEY,
        'redirection_uri': settings.KAKAO_REDIRECT_URL,
        'code': auth_code
    }

    token_response = requests.post(kakao_token_api, data=data).json()
    if token_response.get('error'):
        raise Http404
    
    access_token = token_response.get('access_token')
   

    user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
    

    kakao_nickname = user_info_response.json()['kakao_account']['profile']['nickname']
    kakao_email = user_info_response.json()['kakao_account']['email']

   
    
    return kakao_nickname, kakao_email



class KakaoLoginView(APIView) :
    @swagger_auto_schema(tags=['데이터를 검색합니다.'], request_body=KakaoSerializer, responses=login_res_schema)
    def post(self, request):
        
        kakao_nickname, kakao_email = kakao_access(request)  
        
                                            
        try:
            user = User.objects.get(email=kakao_email)
            
            if user.is_active:
              
                
                user.last_login = timezone.now()
                user.save()
          
                return login(user) 
          
            else:
                return Response(data={'detail': 'blocked user'}, status=status.HTTP_403_FORBIDDEN)
              
            
        except User.DoesNotExist: 
            return Response(data={'detail': 'need to register', 'kakao_nickname': kakao_nickname}, status=status.HTTP_401_UNAUTHORIZED)
            

