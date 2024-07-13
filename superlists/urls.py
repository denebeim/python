from django.urls import include, path
from lists import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("lists/", include("lists.urls")),
]
