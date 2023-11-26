from django.urls import path
from . import views



urlpatterns = [
    path('login',views.KakaoLoginView.as_view()),
     
]