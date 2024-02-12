from django.urls import path

from . import views

urlpatterns = [
    path("list", views.ChatRoomListView.as_view()),
    path("detail", views.ChatRoomDetailView.as_view()),
]
