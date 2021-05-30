from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Stream


# Create your views here.
# The homepage
def home(request):
    streams = Stream.objects.all()
    return render(request, "home.html", {"streams": streams})


@login_required(login_url="/login")
def new_stream(request):
    # TODO: Check if the current user is already streaming
    form = NewStreamForm()
    return render(request, "new_stream.html", {"form": form})


# A class that stores a new stream form
class NewStreamForm(forms.Form):
    stream_name = forms.CharField(label="Stream Name", max_length=100)
    description = forms.CharField(label="Description", max_length=1000)


@require_POST
@login_required(login_url="/login")
def stream(request):
    stream_form = NewStreamForm(request.POST)

    if stream_form.is_valid():
        stream_name = stream_form.cleaned_data["stream_name"]
        description = stream_form.cleaned_data["description"]

        stream = Stream(stream_name=stream_name, user=request.user, description=description,
                        stream_key=get_random_string(30), hls_key=get_random_string(30))
        stream.save()

        return render(request, "stream.html", {"stream": stream})
    else:
        return redirect("new-stream")


# Watch a stream
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
    return HttpResponseRedirect(hls_key)


@require_POST
@csrf_exempt
def stop_stream(request):
    # Will be called when the stream stopped by the nginx rtmp module
    # delete / stop the stream
    Stream.objects.filter(stream_key=request.POST["name"]).delete()
    return HttpResponse("OK")
