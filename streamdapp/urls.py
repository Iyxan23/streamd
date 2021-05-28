from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("watch/<int:stream_id>", views.watch, name="watch"),
]
