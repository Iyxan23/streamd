from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def view(request, user_id=None):
    current_user = None
    if user_id is None:
        # show ourselves
        if not request.user.is_authenticated:
            # not authenticated, redirect to login page
            return HttpResponseRedirect(reverse_lazy('login'))
        else:
            # ok, show our profile
            current_user = request.user
    else:
        # we're viewing other people's profile, find that person's profile
        current_user = get_object_or_404(User, id=user_id)

    return render(request, "showuser.html", {"user": current_user})