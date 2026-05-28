from django.urls import path

from . import views

app_name = "analysis"

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/<str:username>/", views.single_profile, name="single_profile"),
    path("compare/", views.compare, name="compare"),
]
