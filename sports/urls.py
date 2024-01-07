from django.urls import path

from . import views

urlpatterns = [
    path("sports/list", views.SportsListView.as_view()),
    path("weight/list", views.WeightListView.as_view()),
    path("gym/list", views.GymListView.as_view()),
]
