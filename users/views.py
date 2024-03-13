import requests
from django.core.cache import cache
from django.core.exceptions import ValidationError
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
from rest_framework_simplejwt.views import TokenViewBase

from config import settings
from mylib import mysimplejwt
from mylib.nickname import make_random_nickname
from sports.models import Gym

from . import serializers
from .models import BannedUser, Location, User
from .schema import login_res_schema, random_nickname_res_schema, register_res_schema

swagger_tag = "사용자"


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def login(user):
    tokens = get_tokens_for_user(user)

    user_info = serializers.UserInfoSerializer(user)
    user_info = user_info.data
    try:
        user_info["current_location"] = user.user_location.address

    except:
        user_info["current_location"] = None

    res = Response()

    # res.set_cookie(
    #     key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
    #     value=tokens["refresh"],
    #     expires=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
    #     domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
    #     secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
    #     httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
    #     samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
    # )
    res.data = {"refresh": tokens["refresh"], "access": tokens["access"], "user": user_info}

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

    kakao_email = user_info_response.json()["kakao_account"]["email"]

    return kakao_email


class KakaoLoginView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="로그인",
        request_body=serializers.KakaoSerializer,
        responses=login_res_schema,
    )
    # @extend_schema(
    #     tags=[swagger_tag],
    #     summary="로그인",
    #     request=KakaoSerializer,
    #     responses=login_res_schema,
    # )

    def post(self, request):
        """
        user 의 is_active 값을 조절하여 로그인을 차단할 수 있음(is_active를 false로 하면 차단)
        """
        kakao_email = kakao_access(request)

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
                data={"detail": "need to register", "email": kakao_email},
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
        request_body=serializers.UserSerializer,
        responses=register_res_schema,
    )
    def post(self, request):
        """
        BannedUser 를 등록하면 회원가입을 막을 수 있음
        """
        try:
            with transaction.atomic():
                data = request.data.copy()

                gym = data.pop("gym")
                data["sport"] = gym["sport"]

                if BannedUser.objects.filter(email=data["email"]).exists():
                    return Response(status=status.HTTP_403_FORBIDDEN, data="this email is exist in banned user list")

                try:
                    gym_id = Gym.objects.get(
                        name=gym["name"], sport=gym["sport"], latitude=gym["latitude"], longitude=gym["longitude"]
                    ).id

                except Gym.DoesNotExist:
                    serializer = serializers.GymSerializer(data=gym)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    gym_id = serializer.data["id"]

                data["gym"] = gym_id

                serializer = serializers.UserRegisterSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                user_id = serializer.data["id"]

                # location["user"] = user_id

                # serializer = serializers.LocationSerializer(data=location)
                # serializer.is_valid(raise_exception=True)
                # serializer.save()

                user = User.objects.get(id=user_id)
                user.last_login = timezone.now()
                user.save()

                tokens = get_tokens_for_user(user)
                user_info = serializers.UserInfoSerializer(user)
                res = Response()

                # res.set_cookie(
                #     key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                #     value=tokens["refresh"],
                #     expires=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
                #     domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                #     secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                #     httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                #     samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                # )
                res.data = {"refresh": tokens["refresh"], "access": tokens["access"], "user": user_info.data}

                res.status = status.HTTP_201_CREATED

            return res

        except ValidationError as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=[swagger_tag], operation_summary="회원탈퇴")
    def delete(self, request):
        with transaction.atomic():
            user_id = request.user.id

            user = User.objects.get(id=user_id)

            if user.yellow_card == 3:
                BannedUser.objects.create(email=user.email)

            user.delete()

            refreshToken = request.COOKIES.get("refresh")

            token = RefreshToken(refreshToken)
            token.blacklist()
            res = Response()
            res.delete_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"], domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"]
            )
            res.delete_cookie("X-CSRFToken")
            res.delete_cookie("csrftoken")
            # res["X-CSRFToken"]=None
            res.data = {"Success": "Signout successfully"}

            return res


@decorators.permission_classes([permissions.IsAuthenticated])
class LocationView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="유저현재위치 등록/변경",
        request_body=serializers.LocationSerializer,
        responses={"200": "ok", "401": "unauthorized"},
    )
    def post(self, request):
        data = request.data.copy()
        user_id = request.user.id

        data["user"] = user_id

        try:
            location = Location.objects.get(user=user_id)
            serializer = serializers.LocationRegisterSerializer(location, data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except Location.DoesNotExist:
            serializer = serializers.LocationRegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(status=status.HTTP_200_OK)


class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh")
        if attrs["refresh"]:
            # user_id = RefreshToken(attrs["refresh"])["user_id"]
            # WebsocketConnect(user_id)
            return super().validate(attrs)
        else:
            raise jwt_exceptions.InvalidToken("No valid token found in cookie 'refresh'")


class CookieTokenRefreshView(mysimplejwt.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        return super().finalize_response(request, response, *args, **kwargs)


@decorators.permission_classes([permissions.IsAuthenticated])
class LogoutView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag], operation_summary="로그아웃", responses={200: "logout", 401: "unauthorized"}
    )
    def post(self, request):
        try:
            refreshToken = request.COOKIES.get("refresh")

            token = RefreshToken(refreshToken)
            token.blacklist()
            res = Response()
            res.delete_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"], domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"]
            )
            res.delete_cookie("X-CSRFToken")
            res.delete_cookie("csrftoken")
            # res["X-CSRFToken"]=None
            res.data = {"Success": "Logout successfully"}

            return res
        except:
            raise exceptions.ParseError("Invalid token")


@decorators.permission_classes([permissions.IsAuthenticated])
class AccuseView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="사용자 신고",
        request_body=serializers.AccuseRequestSerializer,
        responses={200: "ok", 401: "unauthorized"},
    )
    def patch(self, request):
        """
        사용자 신고 내역은 관리자 페이지에서 관리, 확인 시 admin_confirm 필드를 true로 설정하고
        관리자에 판단에 따라 사용자에게 yellow_card를 부여하거나 is_active를 false로 바꿈
        """
        data = request.data.copy()
        user_id = request.user.id
        data["reporter"] = user_id

        serializer = serializers.AccuseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)
