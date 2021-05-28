# accounts/urls.py
from django.urls import path

from .views import SignUpView, view

app_name = "account"
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("<int:user_id>", view, name="show"), # Show other user's profile
    path("", view, name="show_me"), # Show my profile
]
