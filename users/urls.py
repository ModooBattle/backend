from django.urls import path

from . import views

urlpatterns = [
    path("login", views.KakaoLoginView.as_view()),
    path("logout", views.LogoutView.as_view()),
    path("access", views.CookieTokenRefreshView.as_view()),
    path("random-nickname", views.RandomNicknameView.as_view()),
    path("signup", views.RegisterView.as_view()),
    path("current-location", views.LocationView.as_view()),
    path("accuse", views.AccuseView.as_view()),
]
