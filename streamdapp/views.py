from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string

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


# ==========================================
# views that will be called on stream events

@require_POST
@csrf_exempt
def start_stream(request):
    # Will be called when the stream starts by the nginx rtmp module

    # Find a stream with the matching stream key
    stream = get_object_or_404(Stream, stream_key=request.POST["name"])

    # Check if the stream is streaming :p
    if not stream.is_streaming:
        return HttpResponseForbidden("Already streaming")
    
    # Ok, we're streaming
    stream.is_streaming = True

    # generate a key for the viewers / hls url
    hls_key = get_random_string(30)

    stream.hls_key = hls_key
    stream.save()

    # Now, here comes the hidinng stream key part
    # We will redirect nginx's rtmp module to stream the hls stream into the url we redirected it into
    # So the stream key doesn't get exposed
    return redirect(hls_key)

@require_POST
@csrf_exempt
def stop_stream(request):
    # Will be called when the stream stopped by the nginx rtmp module
    # delete / stop the stream
    Stream.objects.filter(stream_key=request.POST["name"]).delete()
    return HttpResponse("OK")