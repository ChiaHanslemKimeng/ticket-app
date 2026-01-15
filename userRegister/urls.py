from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from userRegister import views

app_name = "userRegister"

urlpatterns = [
    path("", LoginView.as_view(template_name='registerTemplate/login.html'), name="login"),
    path("registrationpage/", views.Register, name="Register"),
    path("logout/", views.logoutview, name="logout"),
]
