from django.urls import path

from . import views

urlpatterns = [
    path("list", views.BoardView.as_view()),
    path("comment", views.CommentView.as_view()),
    path("reply", views.ReplyView.as_view()),
]
