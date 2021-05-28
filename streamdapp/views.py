from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from .models import Stream

# Create your views here.
def home(request):
    streams = Stream.objects.all()
    return render(request, "home.html", {"streams": streams})

def watch(request, stream_id=None):
    if stream_id is None:
        raise Http404()

    stream = get_object_or_404(Stream, pk=stream_id)

    return render(request, "watch.html", {"stream": stream})