from rest_framework import routers
from django.urls import path, include
from boards_app.api.views import BoardListCreateView, EmailCheckView

urlpatterns = [
    path('', BoardListCreateView.as_view()),
    path('email-check/', EmailCheckView.as_view())
]
