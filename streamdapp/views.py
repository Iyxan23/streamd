from django.shortcuts import render
from .models import Stream

# Create your views here.
def home(request):
    streams = Stream.objects.all()
    return render(request, "home.html", {"streams": streams})