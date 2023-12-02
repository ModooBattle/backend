import requests
from django.core.cache import cache
from django.db import transaction
from django.http import Http404
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, exceptions, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import exceptions as jwt_exceptions
from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.tokens import RefreshToken

from config import settings
from mylib.nickname import make_random_nickname

from . import serializers
from .models import User
from .schema import login_res_schema, random_nickname_res_schema
from .serializers import KakaoSerializer, UserSerializer

swagger_tag = "사용자"


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def login(user):
    tokens = get_tokens_for_user(user)
    res = Response()
    serializer = serializers.UserInfoSerializer(user)

    res.set_cookie(
        key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
        value=tokens["refresh"],
        expires=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
    )
    res.data = {"tokens": tokens, "user": serializer.data}

    res.status = status.HTTP_200_OK

    # WebsocketConnect(user.id)

    return res


def kakao_access(request):
    serializer = serializers.KakaoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    auth_code = serializer.validated_data["code"]

    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.KAKAO_REST_API_KEY,
        "redirection_uri": settings.KAKAO_REDIRECT_URL,
        "code": auth_code,
    }

    token_response = requests.post(kakao_token_api, data=data).json()
    if token_response.get("error"):
        raise Http404

    access_token = token_response.get("access_token")

    user_info_response = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer ${access_token}"}
    )

    kakao_nickname = user_info_response.json()["kakao_account"]["profile"]["nickname"]
    kakao_email = user_info_response.json()["kakao_account"]["email"]

    return kakao_nickname, kakao_email


class KakaoLoginView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag], operation_summary="로그인", request_body=KakaoSerializer, responses=login_res_schema
    )
    def post(self, request):
        kakao_nickname, kakao_email = kakao_access(request)

        try:
            user = User.objects.get(email=kakao_email)

            if user.is_active:
                user.last_login = timezone.now()
                user.save()

                return login(user)

            else:
                return Response(data={"detail": "blocked user"}, status=status.HTTP_403_FORBIDDEN)

        except User.DoesNotExist:
            return Response(
                data={"detail": "need to register", "kakao_nickname": kakao_nickname},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class RandomNicknameView(APIView):
    @swagger_auto_schema(tags=[swagger_tag], operation_summary="랜덤닉네임 생성", responses=random_nickname_res_schema)
    def get(self, request):
        nickname = make_random_nickname()

        return Response(data={"nickname": nickname}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="닉네임 중복검사",
        query_serializer=serializers.NicknameQuerySerializer,
        responses={200: "사용가능한 닉네임", 400: "사용불가한 닉네임"},
    )
    def get(self, request):
        try:
            nickname = request.GET["username"]
            user = User.objects.get(username=nickname)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="회원가입",
        request_body=UserSerializer,
        responses={201: "회원가입 완료", 400: "실패"},
    )
    def post(self, request):
        try:
            with transaction.atomic():
                data = request.data.copy()
                location = data.pop("location", None)

                serializer = serializers.UserRegisterSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                user_id = serializer.data["id"]

                location["user"] = user_id

                serializer = serializers.LocationSerializer(data=location)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        except Exception as ex:
            print(ex)
            return Response(status=status.HTTP_400_BAD_REQUEST)
