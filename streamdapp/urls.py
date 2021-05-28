from django.urls import path

from . import views

def fake_view(*args, **kwargs):
    # This view shouldn't be called, because the url 
    # we "connect" to this view will be served by nginx rtmp module
    raise Exception("This should never be called!")

app_name = "streamdapp"
urlpatterns = [
    path("", views.home, name="home"),
    path("watch/<int:stream_id>", views.watch, name="watch"),
    path("start_stream", views.start_stream, name="start-stream"),
    path("stop_stream", views.stop_stream, name="stop-stream"),
    path("live/<hls_key>/index.m3u8", fake_view, name="hls-url"),
]
