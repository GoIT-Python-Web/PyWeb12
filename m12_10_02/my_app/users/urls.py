from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm
from .views import RegisterView

app_name = "users"

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="signup"),
    path("login/",
         LoginView.as_view(template_name="users/login.html", form_class=LoginForm, redirect_authenticated_user=True),
         name="signin"),
    path("logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"),
]
