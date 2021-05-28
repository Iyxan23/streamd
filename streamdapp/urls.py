from django.urls import path

from . import views

app_name = "streamdapp"
urlpatterns = [
    path("", views.home, name="home"),
    path("watch/<int:stream_id>", views.watch, name="watch"),
]
