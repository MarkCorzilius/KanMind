from django.urls import path
from .views import RegisterView, LoginView, EmailCheckView

urlpatterns = [
    path('registration/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('email-check/', EmailCheckView.as_view())
]
